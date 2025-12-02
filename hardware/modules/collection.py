import json
from django.views.decorators.csrf import csrf_exempt
from hardware.models import UserCollection
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from accounts.modules.utils import token_user_id
import jwt


@csrf_exempt
def create_collection(request):
    try:
        body_json = json.loads(request.body)
        token = body_json.get('token')
        
        if not token:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token参数不能为空'}))
        # 从token中获取user_id
        try:
            user_id = token_user_id(token)
        except jwt.DecodeError:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token无效或已过期'}))
        except Exception as e:
            return HttpResponse(json.dumps({'code': 1, 'data': f'token解析失败: {str(e)}'}))
        
        collect_name = body_json.get('collect_name')
        cpu_id = body_json.get('cpu_id')
        gpu_id = body_json.get('gpu_id')
        disk_count = body_json.get('disk_count')
        cpu_name = body_json.get('cpu_name', '')
        gpu_name = body_json.get('gpu_name', '')
        total_powerConsumption = body_json.get('total_powerConsumption', '')
        supportedMotherboard = body_json.get('supportedMotherboard', '')
        suggestMotherboard = body_json.get('suggestMotherboard', '')

        # 插入数据
        collection_result = UserCollection.objects.create(
            user_id=user_id,
            collect_name=collect_name,
            cpu_id=cpu_id,
            gpu_id=gpu_id,
            disk_count=disk_count,
            cpu_name=cpu_name,
            gpu_name=gpu_name,
            total_powerConsumption=total_powerConsumption,
            supportedMotherboard=supportedMotherboard,
            suggestMotherboard=suggestMotherboard
        )
        print("创建了收藏")
        return HttpResponse(json.dumps({'code': 0, 'data': '创建成功!'}))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求体格式错误，需要JSON格式'}))
    except IntegrityError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求错误，请检查参数'}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'data': f'创建失败: {str(e)}'}))


@csrf_exempt
def get_collection_list(request):
    try:
        body_json = json.loads(request.body)
        token = body_json.get('token')
        
        if not token:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token参数不能为空'}))
        
        # 从token中获取user_id
        try:
            user_id = token_user_id(token)
        except jwt.DecodeError:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token无效或已过期'}))
        except Exception as e:
            return HttpResponse(json.dumps({'code': 1, 'data': f'token解析失败: {str(e)}'}))
        
        # 查询该用户的所有收藏，按创建时间降序排序（最近的在前面）
        collections = UserCollection.objects.filter(user_id=user_id).order_by('-create_time')
        
        # 将查询结果转换为字典列表
        collection_list = []
        for collection in collections:
            collection_list.append({
                'id': collection.id,
                'user_id': collection.user_id,
                'collect_name': collection.collect_name,
                'cpu_id': collection.cpu_id,
                'gpu_id': collection.gpu_id,
                'disk_count': collection.disk_count,
                'cpu_name': collection.cpu_name,
                'gpu_name': collection.gpu_name,
                'total_powerConsumption': collection.total_powerConsumption,
                'supportedMotherboard': collection.supportedMotherboard,
                'suggestMotherboard': collection.suggestMotherboard,
                'create_time': collection.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': collection.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return HttpResponse(json.dumps({'code': 0, 'data': collection_list}, ensure_ascii=False))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求体格式错误，需要JSON格式'}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'data': f'查询失败: {str(e)}'}))


@csrf_exempt
def delete_collection(request):
    try:
        body_json = json.loads(request.body)
        token = body_json.get('token')
        collection_id = body_json.get('collection_id')
        
        if not token:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token参数不能为空'}))
        
        if not collection_id:
            return HttpResponse(json.dumps({'code': 1, 'data': 'collection_id参数不能为空'}))
        
        # 从token中获取user_id
        try:
            user_id = token_user_id(token)
        except jwt.DecodeError:
            return HttpResponse(json.dumps({'code': 1, 'data': 'token无效或已过期'}))
        except Exception as e:
            return HttpResponse(json.dumps({'code': 1, 'data': f'token解析失败: {str(e)}'}))
        
        # 查找该收藏，并验证是否属于该用户
        try:
            collection = UserCollection.objects.get(id=collection_id, user_id=user_id)
        except UserCollection.DoesNotExist:
            return HttpResponse(json.dumps({'code': 1, 'data': '收藏不存在或无权删除'}))
        
        # 删除收藏
        collection.delete()
        return HttpResponse(json.dumps({'code': 0, 'data': '删除成功!'}))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求体格式错误，需要JSON格式'}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'data': f'删除失败: {str(e)}'}))

