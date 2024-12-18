import json
import boto3
import botocore

def get_credentials_from_secrets_manager(secret_name="bedrock/credentials", region_name="us-west-2"):
    """
    从 AWS Secrets Manager 获取凭证
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = json.loads(get_secret_value_response['SecretString'])
        print(f"成功获取凭证，region: {secret.get('region', 'us-west-2')}")
        return secret
    except Exception as e:
        print(f"获取凭证时出错: {str(e)}")
        return None

def get_bedrock_client(credentials):
    """
    创建并返回Bedrock客户端
    """
    if not credentials:
        raise ValueError("未能获取到有效的凭证")
    
    region = credentials.get('region', 'us-west-2')
    print(f"正在创建Bedrock客户端，region: {region}")
    
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=region,
        aws_access_key_id=credentials.get('access_key_id'),
        aws_secret_access_key=credentials.get('secret_access_key')
    )
    return bedrock

def invoke_model(prompt, model_id="us.amazon.nova-lite-v1:0"):
    # us.amazon.nova-pro-v1:0
    """
    调用Bedrock模型 - 使用Nova Lite
    """
    try:
        # 获取凭证
        credentials = get_credentials_from_secrets_manager()
        if not credentials:
            print("无法获取凭证")
            return None
        
        # 获取客户端
        client = get_bedrock_client(credentials)
        
        # 构建请求体
        request_body = {
            "schemaVersion": "messages-v1",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "system": [
                {
                    "text": "You are a helpful AI assistant. Please respond in Chinese."
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 500,
                "top_p": 0.9,
                "top_k": 20,
                "temperature": 0.7
            }
        }
        
        print(f"正在调用模型 {model_id}")
        print(f"请求体: {json.dumps(request_body, ensure_ascii=False, indent=2)}")
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        print("成功获得响应")
        response_body = json.loads(response.get('body').read())
        print(f"响应体: {json.dumps(response_body, ensure_ascii=False, indent=2)}")
        
        # 从响应中提取文本内容 - 更新后的Nova响应格式解析
        if response_body.get('output', {}).get('message', {}).get('content'):
            content = response_body['output']['message']['content']
            if isinstance(content, list) and len(content) > 0:
                return content[0].get('text', '')
        return None
    except botocore.exceptions.ClientError as e:
        print(f"AWS API调用错误: {str(e)}")
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'No message')
        print(f"错误代码: {error_code}")
        print(f"错误信息: {error_message}")
        return None
    except Exception as e:
        print(f"调用模型时出错: {str(e)}")
        print(f"错误类型: {type(e)}")
        return None

def main():
    # 测试调用
    prompt = "你能用中文回答吗？请介绍一下你自己。"
    response = invoke_model(prompt)
    if response:
        print("\n回复：")
        print(response)
    else:
        print("调用失败")

if __name__ == "__main__":
    main()
