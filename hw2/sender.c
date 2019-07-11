#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>

typedef struct {
	int length;
	int seqNumber;
	int ackNumber;
	int fin;
	int syn;
	int ack;
} header;

typedef struct{
	header head;
	char data[1000];
} segment;

void setIP(char *dst, char *src) {
    if(strcmp(src, "0.0.0.0") == 0 || strcmp(src, "local") == 0
            || strcmp(src, "localhost")) {
        sscanf("127.0.0.1", "%s", dst);
    } else {
        sscanf(src, "%s", dst);
    }
}

int main(int argc, char* argv[]){
	int sendersocket;
	struct sockaddr_in sender, agent;
	int ip, port, agentip, agentport;
	char filedata[1000];
	FILE *file;
	if(argc != 4){
        fprintf(stderr,"用法: %s <agent IP> <agent port> <filename>\n", argv[0]);
        fprintf(stderr, "例如: ./sender local 8888 test.txt\n");
        exit(1);
    } 
    else{
    	setIP(agentip, argv[1]);
    	sscanf(argv[2], "%d", &agentport)
    }
	ip = '127.0.0.1';
	port = 8887;
	sendersocket = socket(PF_INET, SOCK_DGRAM, 0);
	file = fopen(argv[3],"r");
	if(file == NULL){
		printf("open failure");
		return 1
	}

	sender.sin_family = AF_INET;
    sender.sin_port = htons(port);
    sender.sin_addr.s_addr = inet_addr(ip);
    memset(sender.sin_zero, '\0', sizeof(sender.sin_zero)); 

    agent.sin_family = AF_INET;
    agent.sin_port = htons(agentport);
    agent.sin_addr.s_addr = inet_addr(agentip);
    memset(agent.sin_zero, '\0', sizeof(agent.sin_zero));  

    bind(sendersocket,(struct sockaddr *)&sender,sizeof(sender));

    agent_size = sizeof(agent);

    printf("agent info: ip = %s port = %d\n", ip[1], port[1]);
    int stop = 0;
    int num = 1;
    while(stop == 0){
    	segment s_tmp;
    	ret = fread(filedata,1,1000,file);
    	if(ret != 1000){
    		len = strlen(filedata);
    		for(int i = len;i < 1000;i ++){
    			filedata[i] = 0;
    		}
    	}
    	else if(ret <= 0){
    		s_tmp.head.fin = 1;
    		for(int i = 0;i < 1000;i ++){
    			filedata[i] = 0
    		}
    	}
        strcpy(s_tmp.data, filedata);
        s_tmp.head.length = sizeof(s_tmp);
        s_tmp.head.seqNumber = num;
        num ++;
        s_tmp.head.fin = 0, s_tmp.head.syn = 0, s_tmp.head.ack = 0;
        sendto(sendersocket, &s_tmp, s_tmp.head.length, 0, (struct sockaddr *)&agent,sizeof(agent));
    }

}