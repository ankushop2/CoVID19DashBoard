from flask import Flask, Markup, render_template
import regress
import scrape
import random
import datetime
app = Flask(__name__)


@app.route('/')
def init():
	stats_list, state_list, confirmed_list, cured_list, death_list = scrape.scrape_now()
	x, y, y_pred, days_pred = regress.final()
	x_actual=[]
	number_of_colors = len(state_list)
	color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
	confirmed_list = [None if v is 0 else v for v in confirmed_list]
	cured_list = [None if v is 0 else v for v in cured_list]
	death_list = [None if v is 0 else v for v in death_list]
	for x_data in x:
		x_actual.append(x_data[0])

	now = datetime.datetime.now()
	dates = []
	for i in range(5):
		dates.append(now+datetime.timedelta(days=i))
	# return render_template('index.html', title='COVID-19 India Dashboard', x=x_actual, y=y.tolist(), y_pred=y_pred.tolist(), days_pred=days_pred,
	#  actual_poly=actual_poly, actual_data=actual_data, confirmed_india=confirmed_india, confirmed_foreign=confirmed_foreign,
	#   confirmed_cured=confirmed_cured, confirmed_deaths=confirmed_deaths, confirmed_data=confirmed_data, cured_data=cured_data, death_data=death_data,
	#   state_list=state_list, color=color, dates=dates)
	return render_template('index.html', title='COVID-19 India Dashboard', x=x_actual, y=y.tolist(), y_pred=y_pred.tolist(), days_pred=days_pred,
	   color=color, dates=dates, state_list=state_list, stats_list=stats_list, confirmed_list=confirmed_list, cured_list=cured_list, death_list=death_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

