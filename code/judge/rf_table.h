#ifndef __RF_TABLE__
#define __RF_TABLE__

#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include "logger.h"

/*
 * RF_table 每个值对应的是该syscall可被调用的次数
 *    取值有3种:
 *      正值: 表示可被调用的次数, 每次调用后会减一(比如fork)
 *      零值: 表示禁止调用(比如open)
 *      负值: 表示不限制该syscall(比如write)
 * 
 * RF_table的初始化由init_RF_table函数完成
 */
short RF_table[1024] = {0};

//根据 RF_* 数组来初始化RF_table
void init_RF_table(char* lang_name)
{
    if (LANG_NOT(RESTRICTED_BY_RF_TABLE)) {
        return;
    }

    if (strlen(lang_name) > 100) {
        exit(3);
    }

    char rf_conf_path[256];
    sprintf(rf_conf_path, "%s/%s_rf.conf",
            problem::langs_conf_dir.c_str(),
            lang_name);

    FILE* f = fopen(rf_conf_path, "r");
    if (!f) {
        exit(9);
    }

    memset(RF_table, 0, sizeof(RF_table));

    short syscall_id, count;
    while (fscanf(f, "%hd %hd", &syscall_id, &count) == 2) {
        RF_table[syscall_id] = count;
    }

    if (feof(f)) {
        // Succeeded.
        fclose(f);
    } else {
        fclose(f);
        exit(9);
    }
}

#endif
