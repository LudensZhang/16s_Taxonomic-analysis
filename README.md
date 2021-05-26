# 16s_Taxonomic-analysis
## 激活qiime环境
```
conda activate qiime2-2021.4
```
## 制作一个manifest表,格式如下
```
sample-id,absolute-filepath,direction
ERR4281016,/data2/public/zhanghaohong/5infant_data/ERR4281016_1.fastq.gz,forward
ERR4281016,/data2/public/zhanghaohong/5infant_data/ERR4281016_2.fastq.gz,reverse
```
## 导入数据
```
qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path manifest.txt --output-path paired-end-demux_test.qza --input-format PairedEndFastqManifestPhred33
```
## 拼接
```
qiime vsearch join-pairs --i-demultiplexed-seqs paired-end-demux_test.qza --o-joined-sequences joined.qza
```
## 拼接后可视化
```
qiime demux summarize --i-data joined.qza --o-visualization joined.qzv
```
## 根据需求去噪
```
qiime deblur denoise-16S  --i-demultiplexed-seqs joined.qza  --p-trim-length 251  --o-table table.qza  --o-representative-sequences rep_set.qza  --o-stats stats.qza --p-sample-stats
```
## 下载分类器
```
wget \
  -O "gg-13-8-99-515-806-nb-classifier.qza" \
  "https://data.qiime2.org/2021.4/common/gg-13-8-99-515-806-nb-classifier.qza"
```
## 物种注释
```
qiime feature-classifier classify-sklearn   --i-classifier gg-13-8-99-515-806-nb-classifier.qza   --i-reads rep_set.qza   --o-classification taxonomy.qza
```
## 查看物种注释
```
qiime metadata tabulate --m-input-file taxonomy.qza --o-visualization taxonomy.qzv
```
## 利用biom完成丰度表
#### 得到物种注释
```
qiime tools export    --input-path taxonomy.qza --output-path taxa
```
##### 修改物种注释适配biom格式
```
sed -i -e '1 s/Feature/#Feature/' -e '1 s/Taxon/taxonomy/' taxa/taxonomy.tsv
```
#### 导出biom表
```
qiime tools export --input-path table.qza --output-path table_exported
```
#### 丰度表生成
```
biom add-metadata    -i table_exported/feature-table.biom    -o table_exported/feature-table_w_tax.biom    --observation-metadata-fp taxa/taxonomy.tsv    --sc-separated taxonomy
```
#### biom转tsv
```
biom convert    -i table_exported/feature-table_w_tax.biom    -o table_exported/feature-table_w_tax.txt    --to-tsv    --header-key taxonomy
```
