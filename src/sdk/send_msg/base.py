from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from django.conf import settings
from abc import ABC, abstractmethod


# 基础工厂类
class BaseFactory(ABC):

    @classmethod
    @abstractmethod
    def create_client(cls):
        raise NotImplementedError("Subclasses should implement this method.")


# 阿里云工厂类
class AliyunFactory(BaseFactory):
    @classmethod
    def create_client(cls) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID
            access_key_id=settings.ALIBABA_CLOUD_ACCESS_KEY_ID,
            # 必填，您的 AccessKey Secret
            access_key_secret=settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = settings.ALIBABA_CLOUD_ENDPOINT
        return Dysmsapi20170525Client(config)


# 腾讯云工厂类（示例代码）
class TencentFactory(BaseFactory):
    @classmethod
    def create_client(cls):
        # 假设你有一个腾讯云的客户端类
        # 这里仅为示例，具体实现取决于你使用的腾讯云 SDK
        pass


# 工厂类管理不同的客户端工厂
class Factory:

    def __init__(self):
        self._factories = {
            'send_msg': AliyunFactory,
            'tencent': TencentFactory
        }

    def get_factory(self, provider_name: str):
        factory = self._factories.get(provider_name)
        if factory is None:
            raise ValueError(f"Factory for provider '{provider_name}' not found.")
        return factory


# 客户端代码示例
def client_code(factory_name: str):
    factory = Factory().get_factory(factory_name)
    client = factory.create_client()
    return client
