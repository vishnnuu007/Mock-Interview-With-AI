from flask import*
from database import*

admin=Blueprint(__name__,'admin')


@admin.route("/admin_home")
def admin_home():
    return render_template('admin.html')

@admin.route("/admin_view_user")
def admin_view_user():
    data={}
    qry="select * from user"
    res=select(qry)
    print(res,"////////////////////////////////////////")
    data['view']=res
    return render_template('admin_view_user.html',data=data)


@admin.route("/role",methods=['post','get'])
def role():

    if 'submit' in request.form:
       role_name=request.form['role_name'] 

       a="insert into roles values(null,'%s')"%(role_name)
       id=insert(a)

    data={}
    qry="select * from roles"
    res=select(qry)
    print(res,"////////////////////////////////////////")
    data['view']=res

    if 'action' in request.args:
        act=request.args['action']
        rid=request.args['id']
        print(act,rid)
        if act == 'update':
            qry1="select * from roles where role_id='%s'"%(rid)
            res1=select(qry1)
            data['upd']=res1
            if 'update' in request.form:
                role_name=request.form['role_name'] 
                qry2="update roles set role_name='%s' where role_id='%s'"%(role_name,rid)
                update(qry2)
                return '''<script>alert("updated successfully");window.location="/role"</script>'''
            

        if act == 'delete':
            qry1="delete from roles where role_id='%s'"%(rid)
            res1=delete(qry1)

            return '''<script>alert("Deleted successfully");window.location="/role"</script>'''

    return render_template('role.html',data=data)

@admin.route("/complaint")
def complaint():
    data={}
    qry="SELECT * FROM complaint INNER JOIN USER ON complaint.sender_id = user.user_id"
    res=select(qry)
    print(res,"////////////////////////////////////////")
    data['view']=res
    return render_template('complaint.html',data=data)


@admin.route("/reply",methods=['post','get'])
def reply():
    cid=request.args['id']
    if 'submit' in request.form:
          role_name=request.form['send_reply']
          a="update complaint set reply='%s' where complaint_id='%s'"%(role_name,cid)
          b=update(a)
          if b:
              return '''<script>alert("Reply Send  successfully");window.location="/complaint"</script>'''

    return render_template('reply.html')

@admin.route("/notification", methods=['post','get'])
def notification():

     if 'Submit' in request.form:
       title=request.form['title'] 
       description=request.form['description']
       a="insert into notification values(null,'%s','%s',curdate())"%(title,description)
       id=insert(a)
       return """<script>alert('Notification sented');window.location="/notification"</script>"""

     return render_template('notification.html')