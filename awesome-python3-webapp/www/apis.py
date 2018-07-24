''' JSON API definition'''
import json,logging,inspect,functools

class Page(object):
    def __init__(self,item_count,page_index=1,page_size=10): #参数依次是：数据库博客总数，初始页，一页显示博客数
        self.item_count=item_count
        self.page_size=page_size
        self.page_count=item_count //page_size+(1 if item_count%page_size >0 else 0)
        if (item_count ==0) or (page_index>self.page_count): #假如数据库没有博客或全部博客总页数不足一页
            self.offset=0
            self.limit=0
            self.page_index=1
        else:
            self.page_index=page_index #初始页
            self.offset=self.page_size *(page_index-1) #当前页数，应从数据库的那个序列博客开始显示
            self.limit=self.page_size  #当前页数，应从数据库的那个序列博客结束像素
        self.has_next=self.page_index<self.page_count  #有否下一页
        self.has_previous=self.page_index>1 #有否上一页
    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (
        self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__=__str__

class APIError(Exception):
    '''
    the base APIError which contains error(required),data(optional)and message(optional)
    '''
    def __init__(self,error,data='',message=''):
        super(APIError,self).__init__(message)
        self.error=error
        self.data=data
        self.message=message

class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid. The data specifies the error field of input form

 # 指示输入值有错误或无效。数据指定错误。
    '''
    def __init__(self,field,message=''):
        super(APIValueError,self).__init__('value:invalid',field,message)

class APIResouceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    # 指示未找到资源。数据指定资源名称
    '''
    def __init__(self,field,message=''):
        super(APIResouceNotFoundError,self).__init__('value notfound',field,message)



class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    # 表明API没有权限。
    '''
    def __init__(self,message=''):
        super(APIPermissionError,self).__init__('permission:forbidden','permission',message)

