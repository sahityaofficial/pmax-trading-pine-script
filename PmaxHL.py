#// © sahityaofficial
#//developer: Sahitya_Sahu  
#//author: SAHITYA SAHU
#//@version=4.5.9

strategy("PMax Explorer", shorttitle="PMEx", overlay=true)
src = input(hl2, title="Source")
Periods = input(title="ATR Length", type=input.integer, defval=10)
Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
mav = input(title="Moving Average Type", defval="EMA", options=["SMA", "EMA", "WMA", "TMA", "VAR", "WWMA", "ZLEMA", "TSF"])
length =input(10, "Moving Average Length", minval=1)
changeATR= input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
showsupport = input(title="Show Moving Average?", type=input.bool, defval=true)
showsignalsk = input(title="Show Crossing Signals?", type=input.bool, defval=true)
showsignalsc = input(title="Show Price/Pmax Crossing Signals?", type=input.bool, defval=false)
highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)
atr2 = sma(tr, Periods)
atr= changeATR ? atr(Periods) : atr2
Var_Func(src,length)=>
    valpha=2/(length+1)
    vud1=src>src[1] ? src-src[1] : 0
    vdd1=src<src[1] ? src[1]-src : 0
    vUD=sum(vud1,9)
    vDD=sum(vdd1,9)
    vCMO=nz((vUD-vDD)/(vUD+vDD))
    VAR=0.0
    VAR:=nz(valpha*abs(vCMO)*src)+(1-valpha*abs(vCMO))*nz(VAR[1])
VAR=Var_Func(src,length)
Wwma_Func(src,length)=>
    wwalpha = 1/ length
    WWMA = 0.0
    WWMA := wwalpha*src + (1-wwalpha)*nz(WWMA[1])
WWMA=Wwma_Func(src,length)
Zlema_Func(src,length)=>
    zxLag = length/2==round(length/2) ? length/2 : (length - 1) / 2
    zxEMAData = (src + (src - src[zxLag]))
    ZLEMA = ema(zxEMAData, length)
ZLEMA=Zlema_Func(src,length)
Tsf_Func(src,length)=>
    lrc = linreg(src, length, 0)
    lrc1 = linreg(src,length,1)
    lrs = (lrc-lrc1)
    TSF = linreg(src, length, 0)+lrs
TSF=Tsf_Func(src,length)
getMA(src, length) =>
    ma = 0.0
    if mav == "SMA"
        ma := sma(src, length)
        ma

    if mav == "EMA"
        ma := ema(src, length)
        ma

    if mav == "WMA"
        ma := wma(src, length)
        ma

    if mav == "TMA"
        ma := sma(sma(src, ceil(length / 2)), floor(length / 2) + 1)
        ma

    if mav == "VAR"
        ma := VAR
        ma

    if mav == "WWMA"
        ma := WWMA
        ma

    if mav == "ZLEMA"
        ma := ZLEMA
        ma

    if mav == "TSF"
        ma := TSF
        ma
    ma
    
MAvg=getMA(src, length)
Pmax_Func(src,length)=>
    longStop = MAvg - Multiplier*atr
    longStopPrev = nz(longStop[1], longStop)
    longStop := MAvg > longStopPrev ? max(longStop, longStopPrev) : longStop
    shortStop = MAvg + Multiplier*atr
    shortStopPrev = nz(shortStop[1], shortStop)
    shortStop := MAvg < shortStopPrev ? min(shortStop, shortStopPrev) : shortStop
    dir = 1
    dir := nz(dir[1], dir)
    dir := dir == -1 and MAvg > shortStopPrev ? 1 : dir == 1 and MAvg < longStopPrev ? -1 : dir
    PMax = dir==1 ? longStop: shortStop
PMax=Pmax_Func(src,length)
plot(showsupport ? MAvg : na, color=#0585E1, linewidth=2, title="Moving Avg Line")
pALL=plot(PMax, color=color.red, linewidth=2, title="PMax", transp=0)
alertcondition(cross(MAvg, PMax), title="Cross Alert", message="PMax - Moving Avg Crossing!")
alertcondition(crossover(MAvg, PMax), title="Crossover Alarm", message="Moving Avg BUY SIGNAL!")
alertcondition(crossunder(MAvg, PMax), title="Crossunder Alarm", message="Moving Avg SELL SIGNAL!")
alertcondition(cross(src, PMax), title="Price Cross Alert", message="PMax - Price Crossing!")
alertcondition(crossover(src, PMax), title="Price Crossover Alarm", message="PRICE OVER PMax - BUY SIGNAL!")
alertcondition(crossunder(src, PMax), title="Price Crossunder Alarm", message="PRICE UNDER PMax - SELL SIGNAL!")
buySignalk = crossover(MAvg, PMax)
plotshape(buySignalk and showsignalsk ? PMax*0.995 : na, title="Buy", text="Buy", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.green, textcolor=color.white, transp=0)
sellSignallk = crossunder(MAvg, PMax)
plotshape(sellSignallk and showsignalsk ? PMax*1.005 : na, title="Sell", text="Sell", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.red, textcolor=color.white, transp=0)
buySignalc = crossover(src, PMax)
plotshape(buySignalc and showsignalsc ? PMax*0.995 : na, title="Buy", text="Buy", location=location.absolute, style=shape.labelup, size=size.tiny, color=#0F18BF, textcolor=color.white, transp=0)
sellSignallc = crossunder(src, PMax)
plotshape(sellSignallc and showsignalsc ? PMax*1.005 : na, title="Sell", text="Sell", location=location.absolute, style=shape.labeldown, size=size.tiny, color=#0F18BF, textcolor=color.white, transp=0)
mPlot = plot(ohlc4, title="", style=plot.style_circles, linewidth=0,display=display.none)
longFillColor = highlighting ? (MAvg>PMax ? color.green : na) : na
shortFillColor = highlighting ? (MAvg<PMax ? color.red : na) : na
fill(mPlot, pALL, title="UpTrend Highligter", color=longFillColor)
fill(mPlot, pALL, title="DownTrend Highligter", color=shortFillColor)
showscr = input(true, title="Show Screener Label")
posX_scr = input(20, title="Pos. Label x-axis")
posY_scr = input(1, title="Pos. Size Label y-axis")
colinput = input(title="Label Color", defval="Blue", options=["White", "Black", "Red", "Green", "Yellow", "Blue"])
col = color.gray
if colinput=="White"
    col:=color.white
if colinput=="Black"
    col:=color.black
if colinput=="Red"
    col:=color.red
if colinput=="Green"
    col:=color.green
if colinput=="Yellow"
    col:=color.yellow
if colinput=="Blue"
    col:=color.blue
dummy0 = input(true, title = "=Backtest Inputs=")
FromDay    = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromMonth  = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromYear   = input(defval = 2005, title = "From Year", minval = 2005)
ToDay      = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToMonth    = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToYear     = input(defval = 9999, title = "To Year", minval = 2006)
Start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)
Finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)
Timerange() =>
    time >= Start and time <= Finish ? true : false
if buySignalk
    strategy.entry("Long", strategy.long,when=Timerange())
if sellSignallk
    strategy.entry("Short", strategy.short,when=Timerange())
t1=input('EURUSD',   title='Symbol 01',type=input.symbol)
t2=input('XAUUSD',    title='Symbol 02',type=input.symbol)
t3=input('AMZN',    title='Symbol 03',type=input.symbol)
t4=input('TSLA',    title='Symbol 04',type=input.symbol)
t5=input('BTCUSDT',    title='Symbol 05',type=input.symbol)
t6=input('ETHBTC',    title='Symbol 06',type=input.symbol)
t7=input('XBTUSD',    title='Symbol 07',type=input.symbol)
t8=input('XRPBTC',    title='Symbol 08',type=input.symbol)
t9=input('THYAO',   title='Symbol 09',type=input.symbol)
t10=input('GARAN',    title='Symbol 10',type=input.symbol)
t11=input('USDTRY',      title='Symbol 11',type=input.symbol)
t12=input('PETKM',      title='Symbol 12',type=input.symbol)
t13=input('AAPL',      title='Symbol 13',type=input.symbol)
t14=input('TUPRS',      title='Symbol 14',type=input.symbol)
t15=input('HALKB',      title='Symbol 15',type=input.symbol)
t16=input('AVAXUSDT',     title='Symbol 16',type=input.symbol)
t17=input('ETHUSDT',    title='Symbol 17',type=input.symbol)
t18=input('UKOIL',    title='Symbol 18',type=input.symbol)
t19=input('ABNB',    title='Symbol 19',type=input.symbol)
t20=input('SISE',    title='Symbol 20',type=input.symbol)
Pmax(Multiplier, Periods) =>
    Up=MAvg-(Multiplier*atr)
    Dn=MAvg+(Multiplier*atr)
    
    TrendUp = 0.0
    TrendUp := MAvg[1]>TrendUp[1] ? max(Up,TrendUp[1]) : Up
    TrendDown = 0.0
    TrendDown := MAvg[1]<TrendDown[1]? min(Dn,TrendDown[1]) : Dn
    Trend = 0.0
    Trend := MAvg > TrendDown[1] ? 1: MAvg< TrendUp[1]? -1: nz(Trend[1],1)
    Tsl = Trend==1? TrendUp: TrendDown
    
    S_Buy = Trend == 1 ? 1 : 0
    S_Sell = Trend != 1 ? 1 : 0
    
    [Trend, Tsl]
[Trend, Tsl] =  Pmax(Multiplier, Periods)
TrendReversal = Trend != Trend[1]
[t01, s01] = security(t1, timeframe.period, Pmax(Multiplier, Periods))
[t02, s02] = security(t2, timeframe.period, Pmax(Multiplier, Periods))
[t03, s03] = security(t3, timeframe.period, Pmax(Multiplier, Periods))
[t04, s04] = security(t4, timeframe.period, Pmax(Multiplier, Periods))
[t05, s05] = security(t5, timeframe.period, Pmax(Multiplier, Periods))
[t06, s06] = security(t6, timeframe.period, Pmax(Multiplier, Periods))
[t07, s07] = security(t7, timeframe.period, Pmax(Multiplier, Periods))
[t08, s08] = security(t8, timeframe.period, Pmax(Multiplier, Periods))
[t09, s09] = security(t9, timeframe.period, Pmax(Multiplier, Periods))
[t010, s010] = security(t10, timeframe.period, Pmax(Multiplier, Periods))
[t011, s011] = security(t11, timeframe.period, Pmax(Multiplier, Periods))
[t012, s012] = security(t12, timeframe.period, Pmax(Multiplier, Periods))
[t013, s013] = security(t13, timeframe.period, Pmax(Multiplier, Periods))
[t014, s014] = security(t14, timeframe.period, Pmax(Multiplier, Periods))
[t015, s015] = security(t15, timeframe.period, Pmax(Multiplier, Periods))
[t016, s016] = security(t16, timeframe.period, Pmax(Multiplier, Periods))
[t017, s017] = security(t17, timeframe.period, Pmax(Multiplier, Periods))
[t018, s018] = security(t18, timeframe.period, Pmax(Multiplier, Periods))
[t019, s019] = security(t19, timeframe.period, Pmax(Multiplier, Periods))
[t020, s020] = security(t20, timeframe.period, Pmax(Multiplier, Periods))
tr01 = t01 != t01[1], up01 = t01 == 1, dn01 = t01 == -1
tr02 = t02 != t02[1], up02 = t02 == 1, dn02 = t02 == -1
tr03 = t03 != t03[1], up03 = t03 == 1, dn03 = t03 == -1
tr04 = t04 != t04[1], up04 = t04 == 1, dn04 = t04 == -1
tr05 = t05 != t05[1], up05 = t05 == 1, dn05 = t05 == -1
tr06 = t06 != t06[1], up06 = t06 == 1, dn06 = t06 == -1
tr07 = t07 != t07[1], up07 = t07 == 1, dn07 = t07 == -1
tr08 = t08 != t08[1], up08 = t08 == 1, dn08 = t08 == -1
tr09 = t09 != t09[1], up09 = t09 == 1, dn09 = t09 == -1
tr010 = t010 != t010[1], up010 = t010 == 1, dn010 = t010 == -1
tr011 = t011 != t011[1], up011 = t011 == 1, dn011 = t011 == -1
tr012 = t012 != t012[1], up012 = t012 == 1, dn012 = t012 == -1
tr013 = t013 != t013[1], up013 = t013 == 1, dn013 = t013 == -1
tr014 = t014 != t014[1], up014 = t014 == 1, dn014 = t014 == -1
tr015 = t015 != t015[1], up015 = t015 == 1, dn015 = t015 == -1
tr016 = t016 != t016[1], up016 = t016 == 1, dn016 = t016 == -1
tr017 = t017 != t017[1], up017 = t017 == 1, dn017 = t017 == -1
tr018 = t018 != t018[1], up018 = t018 == 1, dn018 = t018 == -1
tr019 = t019 != t019[1], up019 = t019 == 1, dn019 = t019 == -1
tr020 = t020 != t020[1], up020 = t020 == 1, dn020 = t020 == -1
pot_label = 'Potential Reversal: \n'
pot_label := tr01    ? pot_label + t1 + '\n'  : pot_label
pot_label := tr02    ? pot_label + t2 + '\n'  : pot_label
pot_label := tr03    ? pot_label + t3 + '\n'  : pot_label
pot_label := tr04    ? pot_label + t4 + '\n'  : pot_label
pot_label := tr05    ? pot_label + t5 + '\n'  : pot_label
pot_label := tr06    ? pot_label + t6 + '\n'  : pot_label
pot_label := tr07    ? pot_label + t7 + '\n'  : pot_label
pot_label := tr08    ? pot_label + t8 + '\n'  : pot_label
pot_label := tr09    ? pot_label + t9 + '\n'  : pot_label
pot_label := tr010    ? pot_label + t10 + '\n'  : pot_label
pot_label := tr011    ? pot_label + t11 + '\n'  : pot_label
pot_label := tr012    ? pot_label + t12 + '\n'  : pot_label
pot_label := tr013    ? pot_label + t13 + '\n'  : pot_label
pot_label := tr014    ? pot_label + t14 + '\n'  : pot_label
pot_label := tr015    ? pot_label + t15 + '\n'  : pot_label
pot_label := tr016    ? pot_label + t16 + '\n'  : pot_label
pot_label := tr017    ? pot_label + t17 + '\n'  : pot_label
pot_label := tr018    ? pot_label + t18 + '\n'  : pot_label
pot_label := tr019    ? pot_label + t19 + '\n'  : pot_label
pot_label := tr020    ? pot_label + t20 + '\n'  : pot_label
scr_label = 'Confirmed Reversal: \n'
scr_label := tr01[1] ? scr_label + t1 + '\n'  : scr_label
scr_label := tr02[1] ? scr_label + t2 + '\n'  : scr_label
scr_label := tr03[1] ? scr_label + t3 + '\n'  : scr_label
scr_label := tr04[1] ? scr_label + t4 + '\n'  : scr_label
scr_label := tr05[1] ? scr_label + t5 + '\n'  : scr_label
scr_label := tr06[1] ? scr_label + t6 + '\n'  : scr_label
scr_label := tr07[1] ? scr_label + t7 + '\n'  : scr_label
scr_label := tr08[1] ? scr_label + t8 + '\n'  : scr_label
scr_label := tr09[1] ? scr_label + t9 + '\n'  : scr_label
scr_label := tr010[1] ? scr_label + t10 + '\n'  : scr_label
scr_label := tr011[1] ? scr_label + t11 + '\n'  : scr_label
scr_label := tr012[1] ? scr_label + t12 + '\n'  : scr_label
scr_label := tr013[1] ? scr_label + t13 + '\n'  : scr_label
scr_label := tr014[1] ? scr_label + t14 + '\n'  : scr_label
scr_label := tr015[1] ? scr_label + t15 + '\n'  : scr_label
scr_label := tr016[1] ? scr_label + t16 + '\n'  : scr_label
scr_label := tr017[1] ? scr_label + t17 + '\n'  : scr_label
scr_label := tr018[1] ? scr_label + t18 + '\n'  : scr_label
scr_label := tr019[1] ? scr_label + t19 + '\n'  : scr_label
scr_label := tr020[1] ? scr_label + t20 + '\n'  : scr_label
up_label = 'Uptrend: \n'
up_label := up01[1] ? up_label + t1 + '\n'  : up_label
up_label := up02[1] ? up_label + t2 + '\n'  : up_label
up_label := up03[1] ? up_label + t3 + '\n'  : up_label
up_label := up04[1] ? up_label + t4 + '\n'  : up_label
up_label := up05[1] ? up_label + t5 + '\n'  : up_label
up_label := up06[1] ? up_label + t6 + '\n'  : up_label
up_label := up07[1] ? up_label + t7 + '\n'  : up_label
up_label := up08[1] ? up_label + t8 + '\n'  : up_label
up_label := up09[1] ? up_label + t9 + '\n'  : up_label
up_label := up010[1] ? up_label + t10 + '\n'  : up_label
up_label := up011[1] ? up_label + t11 + '\n'  : up_label
up_label := up012[1] ? up_label + t12 + '\n'  : up_label
up_label := up013[1] ? up_label + t13 + '\n'  : up_label
up_label := up014[1] ? up_label + t14 + '\n'  : up_label
up_label := up015[1] ? up_label + t15 + '\n'  : up_label
up_label := up016[1] ? up_label + t16 + '\n'  : up_label
up_label := up017[1] ? up_label + t17 + '\n'  : up_label
up_label := up018[1] ? up_label + t18 + '\n'  : up_label
up_label := up019[1] ? up_label + t19 + '\n'  : up_label
up_label := up020[1] ? up_label + t20 + '\n'  : up_label
dn_label = 'Downtrend: \n'
dn_label := dn01[1] ? dn_label + t1 + '\n'  : dn_label
dn_label := dn02[1] ? dn_label + t2 + '\n'  : dn_label
dn_label := dn03[1] ? dn_label + t3 + '\n'  : dn_label
dn_label := dn04[1] ? dn_label + t4 + '\n'  : dn_label
dn_label := dn05[1] ? dn_label + t5 + '\n'  : dn_label
dn_label := dn06[1] ? dn_label + t6 + '\n'  : dn_label
dn_label := dn07[1] ? dn_label + t7 + '\n'  : dn_label
dn_label := dn08[1] ? dn_label + t8 + '\n'  : dn_label
dn_label := dn09[1] ? dn_label + t9 + '\n'  : dn_label
dn_label := dn010[1] ? dn_label + t10 + '\n'  : dn_label
dn_label := dn011[1] ? dn_label + t11 + '\n'  : dn_label
dn_label := dn012[1] ? dn_label + t12 + '\n'  : dn_label
dn_label := dn013[1] ? dn_label + t13 + '\n'  : dn_label
dn_label := dn014[1] ? dn_label + t14 + '\n'  : dn_label
dn_label := dn015[1] ? dn_label + t15 + '\n'  : dn_label
dn_label := dn016[1] ? dn_label + t16 + '\n'  : dn_label
dn_label := dn017[1] ? dn_label + t17 + '\n'  : dn_label
dn_label := dn018[1] ? dn_label + t18 + '\n'  : dn_label
dn_label := dn019[1] ? dn_label + t19 + '\n'  : dn_label
dn_label := dn020[1] ? dn_label + t20 + '\n'  : dn_label
f_colorscr (_valscr ) => 
     _valscr  ? #00000000 : na
     
f_printscr (_txtscr ) => 
     var _lblscr  = label(na), 
     label.delete(_lblscr ), 
     _lblscr  := label.new(
     time + (time-time[1])*posX_scr , 
     ohlc4[posY_scr], 
     _txtscr ,
     xloc.bar_time, 
     yloc.price, 
     f_colorscr (  showscr ),
     textcolor =  showscr ? col : na, 
     size = size.normal, 
     style=label.style_label_center
     )
f_printscr ( scr_label + '\n' + pot_label +'\n' + up_label + '\n' + dn_label)
