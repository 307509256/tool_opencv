CC = g++
# ��ִ���ļ�
TARGET = getfile
# C�ļ�
SRCS = getfile.cpp
# Ŀ���ļ�
OBJS = $(SRCS:.cpp=.o)
# ���ļ�
DLIBS = -lopencv_core -lopencv_imgproc -lopencv_highgui
# ����Ϊ��ִ���ļ�
$(TARGET):$(OBJS)
	$(CC) -o $@ $^ $(DLIBS)  
clean:
	rm -rf $(TARGET) $(OBJS)
# ������� $@����Ŀ���ļ� $< �����һ�������ļ�
%.o:%.cpp
	$(CC) -o $@ -c $<