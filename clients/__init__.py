from clients.replicate import ReplicateClient
from clients.openai import OpenaiChatClient

clients_dict = {
    'Replicate': ReplicateClient,
    'Openai-chat': OpenaiChatClient
}
