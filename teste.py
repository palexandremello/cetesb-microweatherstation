import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
@sched.scheduled_job('interval',minutes=3)
def job():
    from micrometeorologyWeatherStation import cetesb
    vars = ['25','29','63']
    data = "/".join(str(datetime.date.today()).split('-')[::-1])
    df = cetesb.getData(data,data,'288',vars[0],exportcsv=True)
    print(type(df))
    cetesb.CsvToJson(df)
    df['MediaHorária'] = df['MediaHoraria'] * 0.29
    df['MediaHoraria'].plot()

sched.start()