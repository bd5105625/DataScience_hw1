# DataScience_hw1

## Dataset:
* 上年度(2020)全年用電和備轉電量資料，但缺失12月最後15天的資料(CSV)
* 2019~2020/10用電和備轉電量資料(CSV)

為了使資料完整無缺，並將資料擴增到今年三月，透過此[連結](https://www.taipower.com.tw/tc/page.aspx?mid=206&cid=405&cchk=e1726094-d08c-431e-abee-05665ab1c974)，
有台電提供的曲線圖，能查看每日的供電和用電數值，逐一查看並添加到原缺失的CSV檔案內。

## Data Preprocessing:

因為提供的資料集為CSV檔案，使用pandas的功能來處理CSV資料，選取特定column:備轉容量(MW)就能一次取得整行的備轉容量資料。
兩個CSV的備轉容量單位不同，可以透過dataframe.map(lambda x:)來做一次整體的運算，使程式更為簡潔明瞭。

## Model:ARIMA

使用著名的時序預測模型ARIMA來預測未來一周的備轉容量，經過反覆的測試和比較，ARIMA三個超引數(p,d,q)分別選擇(3,1,3)能達到較理想的預測結果。
