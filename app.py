import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

def dataprocessing():
    data2020 = pd.read_csv('2020.csv', encoding='utf8')
    data2019 = pd.read_csv('20192021.csv', encoding='utf8')
    # print(data2020['備轉容量(萬瓩)'])
    # print(data2020)
    data2020['備轉容量(萬瓩)'] = data2020['備轉容量(萬瓩)']*10
    # print(data2020['備轉容量(萬瓩)'])
    reserve2019 = data2019[['日期','備轉容量(MW)']]
    reserve2020 = data2020[['日期','備轉容量(萬瓩)']]
    reserve2020['日期'] = reserve2020['日期'].map(lambda x: ''.join(x.split('/')))
    reserve2020 = reserve2020[['日期', '備轉容量(萬瓩)']][305:]
    # reserve2020.rename(columns={'日期':'日期', '備轉容量(萬瓩)': '備轉容量(MW)'})
    reserve2020.columns=['Data' , 'Operating_reserve(MW)']
    reserve2019.columns=['Data' , 'Operating_reserve(MW)']

    print(reserve2020)
    # print(reserve2020[['日期', '備轉容量(萬瓩)']][305:])
    reservetotal = pd.concat([reserve2019 , reserve2020], ignore_index=True)
    plt.figure('Org')
    plt.plot(reservetotal['Operating_reserve(MW)'], 'blue')
    reservetotal['Operating_reserve(MW)'] = reservetotal['Operating_reserve(MW)'].map(lambda x: 10*x if x < 1000 else x)
    reservetotal.to_csv('training.csv', index=False)

    plt.figure('備轉容量2020')
    plt.plot(reservetotal['Operating_reserve(MW)'], 'blue')
    plt.show()

def constructmodel(df_training):
    print(df_training)
    upcomingdays = [0,0,0,0,0,0,0]
    upcomingdays = pd.Series(upcomingdays)
    print(upcomingdays)
    traindata = df_training["Operating_reserve(MW)"][367:770]
    testdata = df_training["Operating_reserve(MW)"][770:]
    print(traindata)
    model = ARIMA(traindata , order=(3,1,3))
    model_fit = model.fit(disp=0)

    fitted = model.fit(disp=-1)
    fc, se, conf = fitted.forecast(39, alpha=0.05)
    fc_series = pd.Series(fc, index=testdata.index)
    lower_series = pd.Series(conf[:, 0], index=testdata.index)
    upper_series = pd.Series(conf[:, 1], index=testdata.index)
    plt.plot(traindata, label='training')
    plt.plot(testdata, label='actual')
    plt.plot(fc_series, label='forecast')
    plt.fill_between(lower_series.index, lower_series, upper_series, 
                    color='k', alpha=.15)
    plt.title('Forecast vs Actuals')
    plt.legend(loc='upper left', fontsize=8)

    answer = pd.DataFrame({
            "date": ['20210323', '20210324', '20210325', '20210326', '20210327', '20210328', '20210329'],
            "Operating_reserve(MW)": fc_series[0:7].map(lambda x: int(x))
    }
    )
    print(answer)
    print(type(answer))
    print(model_fit.summary())
    return answer

if __name__ == '__main__':
    # You should not modify this part, but additional arguments are allowed.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')

    parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
    args = parser.parse_args()

    df_training = pd.read_csv(args.training)
    output = constructmodel(df_training)
    output.to_csv(args.output, index=0)

