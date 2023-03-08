用咒語召喚ChatGPT寫個python flask轉檔服務
==

# 執行方式

```bash
python3 -m venv webapp

cd webapp

. bin/activate

pip install -r requirement.txt

python (app1.py|app2.py|...|app10.py)


```

# 添加允許轉換的來源網域

app6.py 之後可以設定config.ini來限制可訪問的來源網域

```bash
[app]
allowed_domains = example.com, example.co
```

# URL訪問格式

轉換為webp格式

`http://127.0.0.1:5001/webp/TARGET_IMAGE_URL`

resize （依比例轉換與指定長寬）

`http://127.0.0.1:5001/500x0/TARGET_IMAGE_URL`

`http://127.0.0.1:5001/500x200/TARGET_IMAGE_URL`

轉換為webp格式且resize

`http://127.0.0.1:5001/webp/500x0/TARGET_IMAGE_URL`

# 咒語歷程（請自行轉換成英文跟ChatGPT談心）

## app1.py

用python flask寫一個web服務，訪問外部連結並轉換成webp格式。

## app2.py

使用python實作一個圖檔resize的服務。

## app3.py

合併兩個服務，可以resize，也可以轉換為webp。

## app4.py

僅處理jpg格式的轉檔。

## app5.py

加入png格式的支援，並可使用thread。

## app6.py

用設定檔設置允許的外部網域，不允許的不處理。

## app7.py

針對長乘寬進行優化，若其一包含0的數值，就使用比率進行縮圖。

## app8.py

針對app7進行再優化，並提供建議。

## app9.py

加入error control並優化。

## app10.py

非png, jpg就回應外部網站的原始圖檔。

修正原始圖檔為webp進行resize的錯誤。

如果原始圖檔為webp格式，就不再轉換為jpg，僅resize。


結論
==

有了GPT，咒語念得好，程式寫到老。（誤






