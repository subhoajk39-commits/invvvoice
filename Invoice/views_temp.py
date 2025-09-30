@login_required
def get_user_report_view(request, user_id):
    try:
        print(f"[DEBUG] get_user_report_view called for user_id: {user_id}")
        print(f"[DEBUG] Requesting user role: {request.user.role}")
        
        if request.user.role not in ['admin', 'super_admin']:
            print("[DEBUG] Authorization failed - invalid role")
            return JsonResponse({'error': 'Unauthorized - Invalid role'}, status=403)

        user = get_object_or_404(User, id=user_id)
        print(f"[DEBUG] Found user: {user.username}")
        
        # Check permissions
        if request.user.role == 'admin' and user.created_by != request.user:
            print("[DEBUG] Authorization failed - admin permission check")
            return JsonResponse({'error': 'Unauthorized - Invalid permissions'}, status=403)

        # Get user's login history
        login_history = UserLoginHistory.objects.filter(user=user).order_by('-login_datetime')
        print(f"[DEBUG] Found {login_history.count()} login history records")
        
        # Get projects created by user
        projects_created = ClientProject.objects.filter(created_by=user).order_by('-start_date')
        print(f"[DEBUG] Found {projects_created.count()} projects created")
        
        # Get projects managed by user (if admin)
        projects_managed = ClientProject.objects.filter(managed_by=user).order_by('-start_date')
        print(f"[DEBUG] Found {projects_managed.count()} projects managed")
        
        # Get work entries with related data
        work_entries = WorkEntry.objects.filter(user=user).select_related(
            'project', 'category'
        ).order_by('-date')
        print(f"[DEBUG] Found {work_entries.count()} work entries")
        
        # Get work entries statistics
        work_stats = WorkEntry.objects.filter(user=user).aggregate(
            total_entries=models.Count('id'),
            total_quantity=models.Sum('quantity')
        )
        
        # Get project statistics
        project_stats = {}
        for entry in work_entries:
            if entry.project.id not in project_stats:
                project_stats[entry.project.id] = {
                    'name': entry.project.name,
                    'total_entries': 0,
                    'total_quantity': 0
                }
            project_stats[entry.project.id]['total_entries'] += 1
            project_stats[entry.project.id]['total_quantity'] += entry.quantity

        # Prepare user data
        data = {
            'username': user.username,
            'role': user.get_role_display(),
            'created_by': user.created_by.username if user.created_by else None,
            'date_joined': user.date_joined.strftime('%Y-%m-%d'),
            
            # User summary
            'summary': {
                'total_work_entries': work_stats['total_entries'] or 0,
                'total_quantity': work_stats['total_quantity'] or 0,
                'projects_created_count': projects_created.count(),
                'projects_managed_count': projects_managed.count() if user.role in ['admin', 'super_admin'] else 0,
            },
            
            # Login history
            'login_history': [
                {
                    'datetime': timezone.localtime(lh.login_datetime).strftime('%Y-%m-%d %H:%M:%S'),
                    'ip_address': lh.ip_address,
                    'device': f"{lh.os} on {lh.browser}",
                    'browser': lh.browser,
                    'os': lh.os
                } for lh in login_history
            ],
            
            # Projects created by user
            'projects_created': [
                {
                    'name': p.name,
                    'start_date': p.start_date.strftime('%Y-%m-%d'),
                    'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else 'Ongoing',
                    'managed_by': p.managed_by.username if p.managed_by else None,
                    'categories_count': p.categories.count()
                } for p in projects_created
            ],
            
            # Projects managed (if admin)
            'projects_managed': [
                {
                    'name': p.name,
                    'start_date': p.start_date.strftime('%Y-%m-%d'),
                    'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else 'Ongoing',
                    'created_by': p.created_by.username,
                    'categories_count': p.categories.count()
                } for p in projects_managed
            ] if user.role in ['admin', 'super_admin'] else [],
            
            # Work entries
            'work_entries': [
                {
                    'date': we.date.strftime('%Y-%m-%d %H:%M'),
                    'project': we.project.name,
                    'category': we.category.name if we.category else 'N/A',
                    'folder_name': we.folder_name,
                    'quantity': we.quantity,
                    'rate': float(we.category.rate) if we.category else 0,
                    'currency': we.category.currency if we.category else 'USD'
                } for we in work_entries
            ],
            
            # Project-wise statistics
            'project_statistics': [
                {
                    'project_name': stats['name'],
                    'total_entries': stats['total_entries'],
                    'total_quantity': stats['total_quantity']
                } for project_id, stats in project_stats.items()
            ]
        }

        print(f"[DEBUG] Successfully prepared data for user {user.username}")
        return JsonResponse(data)
        
    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)