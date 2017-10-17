/*
 * author: gongjia
 * data: 2017/9/29 
*/

#include <stdio.h>
#include <string.h>
#include <iostream>
#include <algorithm>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>


#if defined(WIN32) || defined(_WIN32)
#include <io.h>
#else
#include <dirent.h>
#endif

//if you want file name start with 01000.jpg, define 1000
#define 			INDEX_OFFSET 		0

#define 			FILE_LEN 				1000
#define 			MAX_IMG_NUM 		20000 

char img_files[MAX_IMG_NUM][FILE_LEN];

using namespace cv;
using namespace std;

static int getFiles(char *basePath)
{
      DIR *dir;
      struct dirent *ptr;
      int ret = 0;
			int num_of_img = 0;

      if ((dir = opendir(basePath)) == NULL){
            printf("Open dir error...(%s)", basePath);
            return ret;
      }

      while ((ptr = readdir(dir)) != NULL){
            if (strcmp(ptr->d_name, ".") == 0 || strcmp(ptr->d_name, "..") == 0 ) ///current dir OR parrent dir
                  continue;
            else if (ptr->d_type == 8){
                //printf("ptr->d_name=%s, ptr->d_type=%d, ptr->d_reclen=%d\n", ptr->d_name, ptr->d_type, ptr->d_reclen);
                strcpy(img_files[num_of_img++], ptr->d_name);
            }
            else{
                continue;
            }
      }
      closedir(dir);

      return num_of_img;
}

int main()
{
		//source image
    char inpath[] = "in";  
     
    //destination image                            
    char outpath[] = "out";  
     
    char order[FILE_LEN];  
    char input_file[FILE_LEN];       
    IplImage *pSrc = NULL;   
    FILE *fp = NULL;                 
    int num, i, index;
    
    fp = fopen("train.txt", "w");

    num = getFiles(inpath);
    printf("file num = %d\n", num);

    for (i = 0; i<num; ++i)
    {
        sprintf(input_file, "%s/%s",inpath, img_files[i]);
        printf("%s\n", input_file);
        pSrc = cvLoadImage(input_file);
        
        if(!pSrc){
        	printf("check your input file path\n");
      	}
      	index = i+INDEX_OFFSET;
        sprintf(order, "%s/%05d.jpg",outpath, index);
        fprintf(fp, "%05d\n", index);
        cvSaveImage(order, pSrc);
        printf("Saving %s!\n", order);
        cvReleaseImage(&pSrc);
    }
    fclose(fp);
    return 0;
}