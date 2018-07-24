import asyncio,os,inspect,logging,functools
from urllib import parse
from aiohttp import web
from www.apis import APIError



def get(path):
    '''
    # Define decorator @get('/path')
    # 定义装饰器获取（'/PATH）
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='GET' #存储方法信息
        wrapper.__route__=path #存储路径信息
        return wrapper
    return decorator

def post(path):
    '''
     # Define decorator @post('/path')
     # 定义装饰器@ POST（'/PATH）
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='POST'
        wrapper.__route__=path
        return wrapper
    return decorator
#使用inspect模块，检查视图函数的参数
#inspect.Parameter.kind类型:
#keyword_only  命名关键字参数
#var_positional  可选参数 *args
#var_keyword   关键字参数 **kw
#positional_or_keyword 位置或必选参数


def get_required_kw_args(fn):   #获取无默认值的命名关键字参数
    args=[]
    ''''' 
    def foo(a, b = 10, *c, d,**kw): pass 
    sig = inspect.signature(foo) ==> <Signature (a, b=10, *c, d, **kw)> 
    sig.parameters ==>  mappingproxy(OrderedDict([('a', <Parameter "a">), ...])) 
    sig.parameters.items() ==> odict_items([('a', <Parameter "a">), ...)]) 
    sig.parameters.values() ==>  odict_values([<Parameter "a">, ...]) 
    sig.parameters.keys() ==>  odict_keys(['a', 'b', 'c', 'd', 'kw']) 
    '''
    params=inspect.signature(fn).parameters  #keyword_only 命名关键字参数
    for name,param in params.items(): #如果视图函数存在命名关键字参数，且默认值为空，获取它的key（参数名）
        if param.kind==inspect.Parameter.KEYWORD_ONLY and param.default ==inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):  #获取命名关键词参数
    args=[]
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind==inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)
def has_named_kw_args(fn):  # 判断是否有命名关键词参数
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind==inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):  # 判断是否有关键词参数
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind ==inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):   # 判断是否含有名叫'request'的参数，且位置在最后
    sig=inspect.signature(fn)
    params=sig.parameters
    found=False
    for name,param in params.items():
        if name=='request':
            found=True
            continue #跳出当前循环，进入下一个循环
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY
        and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function:%s%s')%(fn.__name__,str(sig))
        return found


class RequestHandler(object):
    def __init__(self,app,fn):
        self.__app=app
        self.__func=fn
        self.__has_request_arg=has_request_arg(fn)  # 判断是否含有名叫'request'的参数，且位置在最后
        self.__has_var_kw_arg=has_var_kw_arg(fn)  # 判断是否有关键词参数
        self.__has_named_kw_args=has_named_kw_args(fn) #判断是否有命名关键词参数
        self.__named_kw_args=get_named_kw_args(fn)  #获取命名关键词参数
        self.__required_kw_args=get_required_kw_args(fn)  #获取无默认值的命名关键字参数

    # 1.定义kw，用于保存参数
    # 2.判断视图函数是否存在关键词参数，如果存在根据POST或者GET方法将request请求内容保存到kw
    # 3.如果kw为空（说明request无请求内容），则将match_info列表里的资源映射给kw；若不为空，把命名关键词参数内容给kw
    # 4.完善_has_request_arg和_required_kw_args属性
    async def __call__(self, request):
        kw=None # 定义kw，用于保存request中参数
        if self.__has_var_kw_arg or self.__has_named_kw_args or self.__required_kw_args: #若视图函数有命名关键词或关键词参数
            if request.method == 'POST':
                if  not request.content_type:
                    return web.HTTPBadRequest(text='Missing content-type')
                ct=request.content_type.lower()
                if ct.startswith('application/json'):
                    params=await request.json()
                    if not isinstance(params,dict):
                        return web.HTTPBadRequest(text='json body must be object')
                    kw=params
                elif ct.startswith('application/x-www-form-urlencoded')or ct.startswith('multipart/form-data'):
                    params=await request.post()
                    kw=dict(**params)
                else:
                    return web.HTTPBadRequest(text='unsupported content_type:%s'%request.content_type)
            if request.method =='GET':
                qs=request.query_string
                if qs:
                    kw=dict()
                    for k,v in parse.parse_qs(qs,True).items():
                        kw[k]=v[0]
        if kw is None:
            kw=dict(**request.match_info)
        else:
            if not self.__has_var_kw_arg and self.__named_kw_args: #若视图函数只有命名关键词参数没有关键词参数
                copy=dict()
                for name in self.__named_kw_args:
                    if name in kw:
                        copy[name]=kw[name]
                kw=copy
            for k,v in request.match_info.items():
                if k in kw:
                    logging.info('duplicate arg name in named arg and kw args:%s'%k)
        if self.__has_request_arg:
            kw['request']=request

        if self.__required_kw_args:
            for name in self.__required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest(text='missing  argument:%s'%name)
        logging.info('call with args:%s'%str(kw))
        try:
            r=await self.__func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error,data=e.data,message=e.message)




def add_static(app):
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')
    print(path)
    app.router.add_static('/static/',path)
    logging.info('add static %s =>%s'%('/static/',path))


def add_route(app,fn):
    method=getattr(fn,'__method__',None)
    path=getattr(fn,'__route__',None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s'%str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.iscoroutinefunction(fn):
        fn=asyncio.coroutine(fn)

    logging.info('add route %s %s=>%s %s'%(method,path,fn.__name__,','.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method,path,RequestHandler(app,fn))


def add_routes(app,module_name):
    n=module_name.rfind('.')
    if n==(-1):
        mod=__import__(module_name,globals(),locals())
    else:
        name=module_name[n+1:]
        mod=getattr(__import__(module_name[:n],globals(),locals(),[name]),name)
        # print(mod)
    for attr in dir(mod):
        if attr.startswith('__'):
            continue
        fn=getattr(mod,attr)
        if callable(fn):
            method=getattr(fn,'__method__',None)
            path=getattr(fn,'__route__',None)
            if method and path:
                add_route(app,fn)