# AWS Bedrock Nova Demo

这是一个使用AWS Bedrock Nova服务的示例程序，通过Secrets Manager管理凭证信息。

## 功能特点

- 使用AWS Secrets Manager安全管理凭证
- 支持Nova Lite模型的调用
- 完整的错误处理和日志记录
- 支持中文对话

## 环境要求

- Python 3.7+
- AWS账号
- AWS Bedrock访问权限
- AWS Secrets Manager访问权限

## 设置步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 在AWS Secrets Manager中创建凭证：
   - 登录AWS控制台
   - 进入Secrets Manager服务
   - 创建新的密钥（Secret）
   - 选择"其他类型的密钥"
   - 密钥名称设置为：`bedrock/credentials`
   - 密钥值使用以下JSON格式：
```json
{
    "access_key_id": "你的AWS访问密钥ID",
    "secret_access_key": "你的AWS访问密钥",
    "region": "us-west-2"
}
```

3. 确保运行程序的AWS角色或用户具有以下权限：
   - `secretsmanager:GetSecretValue` - 用于访问Secrets Manager中的凭证
   - `bedrock:InvokeModel` - 用于调用Bedrock模型

## 使用方法

直接运行Python脚本：

```bash
python3 bedrock_demo.py
```

## Nova模型说明

目前支持以下Nova模型：
1. Nova Lite (us.amazon.nova-lite-v1:0) - 默认使用
2. Nova Pro (amazon.nova-pro-v1:0) - 需要创建inference profile才能使用

如果要使用Nova Pro，需要：
1. 在AWS控制台创建inference profile
2. 使用带有inference profile的完整ARN来调用模型

## 代码结构

- `requirements.txt` - 项目依赖
- `bedrock_demo.py` - 主程序代码，包含：
  - Secrets Manager凭证管理
  - Bedrock客户端初始化
  - Nova模型调用
  - 错误处理和日志记录

## 注意事项

- 确保AWS凭证有足够的权限访问Secrets Manager和Bedrock服务
- 使用Nova Pro时需要先创建inference profile
- 代码中包含详细的日志记录，方便调试
- 默认使用us-west-2区域，可以在Secrets Manager中的凭证配置中修改

## 安全建议

- 定期轮换AWS凭证
- 使用最小权限原则配置IAM策略
- 监控和审计Secrets Manager的访问日志
- 不要在代码中硬编码任何凭证信息
