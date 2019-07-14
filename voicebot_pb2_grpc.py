# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import voicebot_pb2 as voicebot__pb2


class VoiceBotStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ListCallCenter = channel.unary_unary(
        '/voicebot.VoiceBot/ListCallCenter',
        request_serializer=voicebot__pb2.ListCallCenterRequest.SerializeToString,
        response_deserializer=voicebot__pb2.ListCallCenterResponse.FromString,
        )
    self.CallToBot = channel.stream_stream(
        '/voicebot.VoiceBot/CallToBot',
        request_serializer=voicebot__pb2.VoiceBotRequest.SerializeToString,
        response_deserializer=voicebot__pb2.VoiceBotResponse.FromString,
        )


class VoiceBotServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ListCallCenter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CallToBot(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_VoiceBotServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListCallCenter': grpc.unary_unary_rpc_method_handler(
          servicer.ListCallCenter,
          request_deserializer=voicebot__pb2.ListCallCenterRequest.FromString,
          response_serializer=voicebot__pb2.ListCallCenterResponse.SerializeToString,
      ),
      'CallToBot': grpc.stream_stream_rpc_method_handler(
          servicer.CallToBot,
          request_deserializer=voicebot__pb2.VoiceBotRequest.FromString,
          response_serializer=voicebot__pb2.VoiceBotResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'voicebot.VoiceBot', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
