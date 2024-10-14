# Auto Tor Fix

یک اسکریپت پایتون برای مدیریت و تغییر IP از طریق شبکه Tor. این اسکریپت امکان تغییر IP به صورت اتوماتیک و دستی را با استفاده از Tor فراهم می‌کند.

## ویژگی‌ها

- **حالت اتوماتیک:** تغییر خودکار IP در فواصل زمانی تعریف شده.
- **حالت دستی:** افزودن یا حذف `ip` سفارشی برای استفاده از لوکیشن های مشخص.

## پیش‌نیازها

قبل از اجرای اسکریپت، اطمینان حاصل کنید که پیش‌نیازهای زیر نصب شده‌اند:

- `Python 3`
- `pip3`
- `Tor`
- `requests`
- `requests[socks]`

## نصب ابزار ها

### 1. به‌روزرسانی سیستم

ابتدا سیستم خود را به‌روز کنید:

```
sudo apt update && sudo apt upgrade -y
```
### 2. نصب Python 3 و pip3
اطمینان حاصل کنید که Python 3 و pip3 نصب شده‌اند. اگر نصب نیستند، از دستورات زیر استفاده کنید:
```
sudo apt install python3 python3-pip -y
```
### 3. نصب Tor
```
sudo apt install tor -y
```
### 4. ایجاد و فعال‌سازی محیط مجازی

نصب ابزار venv :
```
sudo apt install python3-venv -y
```
ایجاد محیط مجازی :
```
python3 -m venv myenv
```
فعال‌سازی محیط مجازی :
پس از فعال‌سازی، نام محیط مجازی (مثلاً myenv) در ابتدای خط فرمان نمایش داده می‌شود.
```
source myenv/bin/activate
```
### 5. نصب ابزارهای پایتونی
با فعال بودن محیط مجازی، ابزار های مورد نیاز اسکریپت رو نصب کنید:
```
pip install --upgrade pip
pip install requests requests[socks]
```
## ران کردن اسکریپت

### 1. کلون کردن مخزن
```
git clone https://github.com/moz3240/Auto-Tor-Fix.git
```
### 2. ورود به دایرکتوری
```
cd Auto-Tor-Fix
```
### 3. نصب اسکریپت روی سرور
```
python3 install.py
```
### 4. اجرا
بعد نصب اسکریپت با این دستور اسکریپت رو اجرا کنید
```
mtor
```
## ست کردن یک آی‌پی خاص ( دستی )

1- اول از همه حالت `manual` رو انتخاب کنید<br>
2- سپس `Add ip` رو انتخاب کنید <br>
3- یک آیپی دلخواه از [لیست](iplist.txt) انتخاب کنید<br>
4- وارد این [سایت](https://metrics.torproject.org/rs.html) بشید و اون آیپی رو سرچ کنید<br>
5- بعد چک کنید ببنید آیا اون آیپی آنلاینه یا نه<br>
6- بعدش میتونید ازش استفاده کنید<br>
7- آیپی رو در اسکریپت وارد کنید و بعد `N` رو تایپ کنید. ✔️<br> 

"آی‌پی‌های زیادی از کشورهای مختلف وجود داره که می‌تونید به راحتی تنظیمشون کنید و به صورت ثابت از اون لوکیشن استفاده کنید."

نکته : اگه اسکریپت بسته شد خواستید دوباره اجراش کنید فقط کافیه اول محیط مجازی رو فعال کنید و بعد mtor رو تایپ کنید.




♡
