拼音输入法
====
一、项目结构
--
*学习语料=textlib*

   可通过readme最后的网盘链接获取。
* database_lib:语料库
* spell2char:拼音汉字表及一二级汉字表
* testlib:测试语料

*代码文件-src*

   将整个识别过程划分为格式化文本、统计出现频率、使用viterbi算法进行拼音转化三个步骤，便于对每一步单独进行调试。按照顺序单独执行每个文件即可，也可以使用run.py直接连续运行三个文件，前两部分用时较长。
* data_format.py:读取语料库内容，并将其切分、格式化为纯汉字文本
* freq_count.py:读取spell2char中的一二级汉字表中的全部汉字，学习data_format中的标准语料。统计各个汉字的出现频次及所有出现的二元词频次并存放在json文件中。
* translator.py:通过读取频次表计算概率。translate函数实现了基于二元模型的viterbi算法，接受拼音文件并输出为output。

语料素材链接：https://pan.baidu.com/s/16ruBIGMtTwEC1Foh3KHeEw  提取码：5186 

--素材来自马少平老师人工智能导论课件
