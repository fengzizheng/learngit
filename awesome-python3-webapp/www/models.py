import time,uuid
from www.orm import Model,StringField,BooleanField,FloatField,TextField
from www import orm
import asyncio,logging
logging.basicConfig(level=logging.INFO)
def next_id():
    return '%015d%s000'%(int(time.time()*1000),uuid.uuid4().hex)

class User(Model):
    __table__ ='users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)


# if __name__ =="__main__":
#     def test():
#         yield from orm.create_pool(loop=loop,user="root", password="root", db="test",host="localhost",port="3306")
#         u = User(name="lili", email="zizhen@qq.com", passwd='123456', image='http://www.baidu.com')
#         yield from u.save()
#         a = yield from u.findAll()
#         print(a)
#     loop=asyncio.get_event_loop()
#     loop.run_until_complete(test())
#     loop.close()
if __name__== '__main__':

    async def test():
        await orm.create_pool(loop=loop,user='root', password='root', db='test')
        # u = User(name='Testtest', email='tedfdsfst@qq.com', passwd='12345', image='about:blank')
        # await u.save()  #插入一条数据
        # a = await u.findAll() #这个要打印才显示出来
        # print(a)
        # b=await u.findAll(where="email='test@qq.com'")#按查询条件查找
        # print(b)
        # c=await u.findNumber(selectField="count(*)") # 集合函数查找
        # print(c)
        # d=await User.find(pk="0015303633410916cba62ec99bf4a07b92346b31ad5ad7d000") #查找主键
        # print(d)
        # u=User(id='0015292393257633defd31962284d4a82a71490e8f73026000') #删除一条id='？'记录
        # await u.remove()
        # u = User(name='Testtest', email='tedfdsfst@qq.com', passwd='12345', image='about:blank',id='001521294117200993ecd9cf5614d42997c03a18a72e33a000',
        #          admin="0",created_at='1')#修改一条记录
        # await u.update()
        d= await User.find('001521294117200993ecd9cf5614d42997c03a18a72e33a0000')
        await d.remove()





    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # www.orm.__pool.close()  #在关闭event loop之前，首先需要关闭连接池。
    # loop.run_until_complete(www.orm.__pool.wait_closed())#在关闭event loop之前，首先需要关闭连接池。
    # loop.close()