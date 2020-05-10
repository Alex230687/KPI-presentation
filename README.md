# KPI-presentaion

Python stack:
python 3.6.5 / django 2.1.7 / django-bootstrap 1.1.1 / django-pandas 0.6.1 / pandas /\n

Authorization:
admin - admin_main@mail.ru / 1234
user1 - user2@mail.ru / ca4hjzlmsq
user2 - user3@mail.ru / asd123asd

Base KPI project contatins 30 indicators for 25 managers.
Short version contatins indicators from main 4 groups - value, percent, turnover, variable.
Value indicator = Sum(rows)
Percent indicator = Sum(numerator rows) / Sum(denominator rows)
Turnover indicator = Avr(12month numerator rows) / Avr(12month denominator rows)
Variable indicator = Sum(fixed rows) + (Sum(variable rows) * Revenue implementation %)

Users are divided into three types:
Manager - has access only to own dashboard page and indicator page from his indicator list
Director - has access for all urls of all users, but doesn't have own dashboard page
Director/Manager - has access for all urls of all users, and has own dashboard page

To set current period is use CurrentPeriod model.
On dashboard page indicator is calculating as current period YTD slice.
On indicator page i select current period, but it is possible to form table with YDT or by month data.
Also on indicator page possible to form forecast data. In this case until current period will be Actual data, after Forecast data.

##################################################


Celery block added.
Mongoengine block added.

Create simple celery task for logging form queries from indicator page.
