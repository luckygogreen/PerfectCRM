#判断当前登录用户的客户
def view_my_own_customers(request):
    print('This is permission_hook.view_my_own_customers 方法',request.user.id)
    if str(request.user.id) == request.GET.get('cunsultant'):
        print('访问的是自己的客户')
        return True
    else:
        print('不能访问他人的客户')
        return False