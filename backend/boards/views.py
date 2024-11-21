from rest_framework.response import Response

from django.shortcuts import render
from django.http import JsonResponse

from .serializers import BoardListSerializer, BoardSerializer
from .models import Board
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# 게시글 생성(POST), 전체 게시글 조회(GET)
@api_view(['GET', 'POST'])
def board_list(request):
    if request.method == 'POST':
        # 사용자로부터 받은 입력을 포장
        serializer = BoardListSerializer(data=request.data)
        # 포장된 데이터가 모두 정상적일 때(유효성 검증을 통과했을 때),
        if serializer.is_valid():
            # 사용자 입력이 아닌 다른 필드들을 함께 저장하도록 코드를 구성
            serializer.save(writer=request.user)
            return Response(serializer.data)
    else:
        boards = Board.objects.all().order_by('-pk')
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data)

# 게시글 삭제(DELETE) 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def delete_board(request, board_id):
    try:
        # 게시글 객체 가져오기
        board = Board.objects.get(id=board_id)

        # 요청자가 작성자인지 확인
        if request.user != board.writer:
            return Response(
                {"error": "삭제 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 게시글 삭제
        board.delete()
        return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

    except Board.DoesNotExist:
        # 게시글이 없는 경우 404 응답 반환
        return Response({"error": "게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 게시글 수정 - 작성자 확인 후 삭제(토큰)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def update_board(request, board_id):
    try:
        # 수정할 게시글 가져오기
        board = Board.objects.get(id=board_id)

        # 요청자가 게시글 작성자인지 확인
        if request.user != board.writer:
            return Response(
                {"error": "수정 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 요청 데이터를 사용하여 게시글 수정
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Board.DoesNotExist:
        # 게시글이 없는 경우
        return Response({"error": "게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)