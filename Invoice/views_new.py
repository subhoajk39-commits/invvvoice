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

        login_history = UserLoginHistory.objects.filter(user=user).order_by('-login_datetime')[:10]
        print(f"[DEBUG] Found {login_history.count()} login history records")
        
        projects_created = ClientProject.objects.filter(created_by=user).order_by('-start_date')
        print(f"[DEBUG] Found {projects_created.count()} projects")
        
        work_entries = WorkEntry.objects.filter(user=user).select_related('project', 'category').order_by('-date')[:20]
        print(f"[DEBUG] Found {work_entries.count()} work entries")

        # Prepare user data
        data = {
            'username': user.username,
            'role': user.get_role_display(),
            'created_by': user.created_by.username if user.created_by else None,
            'date_joined': user.date_joined.strftime('%Y-%m-%d'),
            'login_history': [
                {
                    'datetime': timezone.localtime(lh.login_datetime).strftime('%Y-%m-%d %H:%M:%S'),
                    'ip_address': lh.ip_address,
                    'device': f"{lh.os} on {lh.browser}"
                } for lh in login_history
            ],
            'projects_created': [
                {
                    'name': p.name,
                    'start_date': p.start_date.strftime('%Y-%m-%d')
                } for p in projects_created
            ],
            'work_entries': [
                {
                    'date': we.date.strftime('%Y-%m-%d'),
                    'project': we.project.name,
                    'category': we.category.name if we.category else 'N/A',
                    'folder_name': we.folder_name,
                    'quantity': we.quantity
                } for we in work_entries
            ]
        }
        print(f"[DEBUG] Successfully prepared data for user {user.username}")
        return JsonResponse(data)
        
    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)