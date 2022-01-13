# Generated by Django 3.2.7 on 2022-01-13 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='user3.jpg', null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('portfolio_id', models.AutoField(primary_key=True, serialize=False)),
                ('portfolio_title', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('p_shares_num_sum', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=999, null=True)),
                ('p_last_mod_date', models.DateField(blank=True, null=True)),
                ('p_comp_num_sum', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=999, null=True)),
                ('p_to_buy_percentage', models.CharField(blank=True, max_length=200, null=True)),
                ('p_profit_earned', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=999, null=True)),
                ('user_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='optifolio.customer')),
            ],
        ),
        migrations.CreateModel(
            name='TicName',
            fields=[
                ('tic_sym', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False)),
                ('tic_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VisData',
            fields=[
                ('visdata_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('title2', models.CharField(choices=[('A', 'A'), ('AAL', 'AAL'), ('AAP', 'AAP'), ('AAPL', 'AAPL'), ('ABBV', 'ABBV'), ('ABC', 'ABC'), ('ABMD', 'ABMD'), ('ABT', 'ABT'), ('ACN', 'ACN'), ('ADBE', 'ADBE'), ('ADI', 'ADI'), ('ADM', 'ADM'), ('ADP', 'ADP'), ('ADSK', 'ADSK'), ('AEE', 'AEE'), ('AEP', 'AEP'), ('AES', 'AES'), ('AFL', 'AFL'), ('AIG', 'AIG'), ('AIZ', 'AIZ'), ('AJG', 'AJG'), ('AKAM', 'AKAM'), ('ALB', 'ALB'), ('ALGN', 'ALGN'), ('ALK', 'ALK'), ('ALL', 'ALL'), ('ALLE', 'ALLE'), ('AMAT', 'AMAT'), ('AMCR', 'AMCR'), ('AMD', 'AMD'), ('AME', 'AME'), ('AMGN', 'AMGN'), ('AMP', 'AMP'), ('AMT', 'AMT'), ('AMZN', 'AMZN'), ('ANET', 'ANET'), ('ANSS', 'ANSS'), ('ANTM', 'ANTM'), ('AON', 'AON'), ('AOS', 'AOS'), ('APA', 'APA'), ('APD', 'APD'), ('APH', 'APH'), ('APTV', 'APTV'), ('ARE', 'ARE'), ('ATO', 'ATO'), ('ATVI', 'ATVI'), ('AVB', 'AVB'), ('AVGO', 'AVGO'), ('AVY', 'AVY'), ('AWK', 'AWK'), ('AXP', 'AXP'), ('AZO', 'AZO'), ('BA', 'BA'), ('BAC', 'BAC'), ('BAX', 'BAX'), ('BBWI', 'BBWI'), ('BBY', 'BBY'), ('BDX', 'BDX'), ('BEN', 'BEN'), ('BF-B', 'BF-B'), ('BIIB', 'BIIB'), ('BIO', 'BIO'), ('BK', 'BK'), ('BKNG', 'BKNG'), ('BKR', 'BKR'), ('BLK', 'BLK'), ('BLL', 'BLL'), ('BMY', 'BMY'), ('BR', 'BR'), ('BRK-B', 'BRK-B'), ('BRO', 'BRO'), ('BSX', 'BSX'), ('BWA', 'BWA'), ('BXP', 'BXP'), ('C', 'C'), ('CAG', 'CAG'), ('CAH', 'CAH'), ('CARR', 'CARR'), ('CAT', 'CAT'), ('CB', 'CB'), ('CBOE', 'CBOE'), ('CBRE', 'CBRE'), ('CCI', 'CCI'), ('CCL', 'CCL'), ('CDAY', 'CDAY'), ('CDNS', 'CDNS'), ('CDW', 'CDW'), ('CE', 'CE'), ('CERN', 'CERN'), ('CF', 'CF'), ('CFG', 'CFG'), ('CHD', 'CHD'), ('CHRW', 'CHRW'), ('CHTR', 'CHTR'), ('CI', 'CI'), ('CINF', 'CINF'), ('CL', 'CL'), ('CLX', 'CLX'), ('CMA', 'CMA'), ('CMCSA', 'CMCSA'), ('CME', 'CME'), ('CMG', 'CMG'), ('CMI', 'CMI'), ('CMS', 'CMS'), ('CNC', 'CNC'), ('CNP', 'CNP'), ('COF', 'COF'), ('COO', 'COO'), ('COP', 'COP'), ('COST', 'COST'), ('CPB', 'CPB'), ('CPRT', 'CPRT'), ('CRL', 'CRL'), ('CRM', 'CRM'), ('CSCO', 'CSCO'), ('CSX', 'CSX'), ('CTAS', 'CTAS'), ('CTLT', 'CTLT'), ('CTRA', 'CTRA'), ('CTSH', 'CTSH'), ('CTVA', 'CTVA'), ('CTXS', 'CTXS'), ('CVS', 'CVS'), ('CVX', 'CVX'), ('CZR', 'CZR'), ('D', 'D'), ('DAL', 'DAL'), ('DD', 'DD'), ('DE', 'DE'), ('DFS', 'DFS'), ('DG', 'DG'), ('DGX', 'DGX'), ('DHI', 'DHI'), ('DHR', 'DHR'), ('DIS', 'DIS'), ('DISCA', 'DISCA'), ('DISCK', 'DISCK'), ('DISH', 'DISH'), ('DLR', 'DLR'), ('DLTR', 'DLTR'), ('DOV', 'DOV'), ('DOW', 'DOW'), ('DPZ', 'DPZ'), ('DRE', 'DRE'), ('DRI', 'DRI'), ('DTE', 'DTE'), ('DUK', 'DUK'), ('DVA', 'DVA'), ('DVN', 'DVN'), ('DXC', 'DXC'), ('DXCM', 'DXCM'), ('EA', 'EA'), ('EBAY', 'EBAY'), ('ECL', 'ECL'), ('ED', 'ED'), ('EFX', 'EFX'), ('EIX', 'EIX'), ('EL', 'EL'), ('EMN', 'EMN'), ('EMR', 'EMR'), ('ENPH', 'ENPH'), ('EOG', 'EOG'), ('EPAM', 'EPAM'), ('EQIX', 'EQIX'), ('EQR', 'EQR'), ('ES', 'ES'), ('ESS', 'ESS'), ('ETN', 'ETN'), ('ETR', 'ETR'), ('ETSY', 'ETSY'), ('EVRG', 'EVRG'), ('EW', 'EW'), ('EXC', 'EXC'), ('EXPD', 'EXPD'), ('EXPE', 'EXPE'), ('EXR', 'EXR'), ('F', 'F'), ('FANG', 'FANG'), ('FAST', 'FAST'), ('FB', 'FB'), ('FBHS', 'FBHS'), ('FCX', 'FCX'), ('FDS', 'FDS'), ('FDX', 'FDX'), ('FE', 'FE'), ('FFIV', 'FFIV'), ('FIS', 'FIS'), ('FISV', 'FISV'), ('FITB', 'FITB'), ('FLT', 'FLT'), ('FMC', 'FMC'), ('FOX', 'FOX'), ('FOXA', 'FOXA'), ('FRC', 'FRC'), ('FRT', 'FRT'), ('FTNT', 'FTNT'), ('FTV', 'FTV'), ('GD', 'GD'), ('GE', 'GE'), ('GILD', 'GILD'), ('GIS', 'GIS'), ('GL', 'GL'), ('GLW', 'GLW'), ('GM', 'GM'), ('GNRC', 'GNRC'), ('GOOG', 'GOOG'), ('GOOGL', 'GOOGL'), ('GPC', 'GPC'), ('GPN', 'GPN'), ('GPS', 'GPS'), ('GRMN', 'GRMN'), ('GS', 'GS'), ('GWW', 'GWW'), ('HAL', 'HAL'), ('HAS', 'HAS'), ('HBAN', 'HBAN'), ('HCA', 'HCA'), ('HD', 'HD'), ('HES', 'HES'), ('HIG', 'HIG'), ('HII', 'HII'), ('HLT', 'HLT'), ('HOLX', 'HOLX'), ('HON', 'HON'), ('HPE', 'HPE'), ('HPQ', 'HPQ'), ('HRL', 'HRL'), ('HSIC', 'HSIC'), ('HST', 'HST'), ('HSY', 'HSY'), ('HUM', 'HUM'), ('HWM', 'HWM'), ('IBM', 'IBM'), ('ICE', 'ICE'), ('IDXX', 'IDXX'), ('IEX', 'IEX'), ('IFF', 'IFF'), ('ILMN', 'ILMN'), ('INCY', 'INCY'), ('INFO', 'INFO'), ('INTC', 'INTC'), ('INTU', 'INTU'), ('IP', 'IP'), ('IPG', 'IPG'), ('IPGP', 'IPGP'), ('IQV', 'IQV'), ('IR', 'IR'), ('IRM', 'IRM'), ('ISRG', 'ISRG'), ('IT', 'IT'), ('ITW', 'ITW'), ('IVZ', 'IVZ'), ('J', 'J'), ('JBHT', 'JBHT'), ('JCI', 'JCI'), ('JKHY', 'JKHY'), ('JNJ', 'JNJ'), ('JNPR', 'JNPR'), ('JPM', 'JPM'), ('K', 'K'), ('KEY', 'KEY'), ('KEYS', 'KEYS'), ('KHC', 'KHC'), ('KIM', 'KIM'), ('KLAC', 'KLAC'), ('KMB', 'KMB'), ('KMI', 'KMI'), ('KMX', 'KMX'), ('KO', 'KO'), ('KR', 'KR'), ('L', 'L'), ('LDOS', 'LDOS'), ('LEN', 'LEN'), ('LH', 'LH'), ('LHX', 'LHX'), ('LIN', 'LIN'), ('LKQ', 'LKQ'), ('LLY', 'LLY'), ('LMT', 'LMT'), ('LNC', 'LNC'), ('LNT', 'LNT'), ('LOW', 'LOW'), ('LRCX', 'LRCX'), ('LUMN', 'LUMN'), ('LUV', 'LUV'), ('LVS', 'LVS'), ('LW', 'LW'), ('LYB', 'LYB'), ('LYV', 'LYV'), ('MA', 'MA'), ('MAA', 'MAA'), ('MAR', 'MAR'), ('MAS', 'MAS'), ('MCD', 'MCD'), ('MCHP', 'MCHP'), ('MCK', 'MCK'), ('MCO', 'MCO'), ('MDLZ', 'MDLZ'), ('MDT', 'MDT'), ('MET', 'MET'), ('MGM', 'MGM'), ('MHK', 'MHK'), ('MKC', 'MKC'), ('MKTX', 'MKTX'), ('MLM', 'MLM'), ('MMC', 'MMC'), ('MMM', 'MMM'), ('MNST', 'MNST'), ('MO', 'MO'), ('MOS', 'MOS'), ('MPC', 'MPC'), ('MPWR', 'MPWR'), ('MRK', 'MRK'), ('MRNA', 'MRNA'), ('MRO', 'MRO'), ('MS', 'MS'), ('MSCI', 'MSCI'), ('MSFT', 'MSFT'), ('MSI', 'MSI'), ('MTB', 'MTB'), ('MTCH', 'MTCH'), ('MTD', 'MTD'), ('MU', 'MU'), ('NCLH', 'NCLH'), ('NDAQ', 'NDAQ'), ('NEE', 'NEE'), ('NEM', 'NEM'), ('NFLX', 'NFLX'), ('NI', 'NI'), ('NKE', 'NKE'), ('NLOK', 'NLOK'), ('NLSN', 'NLSN'), ('NOC', 'NOC'), ('NOW', 'NOW'), ('NRG', 'NRG'), ('NSC', 'NSC'), ('NTAP', 'NTAP'), ('NTRS', 'NTRS'), ('NUE', 'NUE'), ('NVDA', 'NVDA'), ('NVR', 'NVR'), ('NWL', 'NWL'), ('NWS', 'NWS'), ('NWSA', 'NWSA'), ('NXPI', 'NXPI'), ('O', 'O'), ('ODFL', 'ODFL'), ('OGN', 'OGN'), ('OKE', 'OKE'), ('OMC', 'OMC'), ('ORCL', 'ORCL'), ('ORLY', 'ORLY'), ('OTIS', 'OTIS'), ('OXY', 'OXY'), ('PAYC', 'PAYC'), ('PAYX', 'PAYX'), ('PBCT', 'PBCT'), ('PCAR', 'PCAR'), ('PEAK', 'PEAK'), ('PEG', 'PEG'), ('PENN', 'PENN'), ('PEP', 'PEP'), ('PFE', 'PFE'), ('PFG', 'PFG'), ('PG', 'PG'), ('PGR', 'PGR'), ('PH', 'PH'), ('PHM', 'PHM'), ('PKG', 'PKG'), ('PKI', 'PKI'), ('PLD', 'PLD'), ('PM', 'PM'), ('PNC', 'PNC'), ('PNR', 'PNR'), ('PNW', 'PNW'), ('POOL', 'POOL'), ('PPG', 'PPG'), ('PPL', 'PPL'), ('PRU', 'PRU'), ('PSA', 'PSA'), ('PSX', 'PSX'), ('PTC', 'PTC'), ('PVH', 'PVH'), ('PWR', 'PWR'), ('PXD', 'PXD'), ('PYPL', 'PYPL'), ('QCOM', 'QCOM'), ('QRVO', 'QRVO'), ('RCL', 'RCL'), ('RE', 'RE'), ('REG', 'REG'), ('REGN', 'REGN'), ('RF', 'RF'), ('RHI', 'RHI'), ('RJF', 'RJF'), ('RL', 'RL'), ('RMD', 'RMD'), ('ROK', 'ROK'), ('ROL', 'ROL'), ('ROP', 'ROP'), ('ROST', 'ROST'), ('RSG', 'RSG'), ('RTX', 'RTX'), ('SBAC', 'SBAC'), ('SBNY', 'SBNY'), ('SBUX', 'SBUX'), ('SCHW', 'SCHW'), ('SEDG', 'SEDG'), ('SEE', 'SEE'), ('SHW', 'SHW'), ('SIVB', 'SIVB'), ('SJM', 'SJM'), ('SLB', 'SLB'), ('SNA', 'SNA'), ('SNPS', 'SNPS'), ('SO', 'SO'), ('SPG', 'SPG'), ('SPGI', 'SPGI'), ('SRE', 'SRE'), ('STE', 'STE'), ('STT', 'STT'), ('STX', 'STX'), ('STZ', 'STZ'), ('SWK', 'SWK'), ('SWKS', 'SWKS'), ('SYF', 'SYF'), ('SYK', 'SYK'), ('SYY', 'SYY'), ('T', 'T'), ('TAP', 'TAP'), ('TDG', 'TDG'), ('TDY', 'TDY'), ('TECH', 'TECH'), ('TEL', 'TEL'), ('TER', 'TER'), ('TFC', 'TFC'), ('TFX', 'TFX'), ('TGT', 'TGT'), ('TJX', 'TJX'), ('TMO', 'TMO'), ('TMUS', 'TMUS'), ('TPR', 'TPR'), ('TRMB', 'TRMB'), ('TROW', 'TROW'), ('TRV', 'TRV'), ('TSCO', 'TSCO'), ('TSLA', 'TSLA'), ('TSN', 'TSN'), ('TT', 'TT'), ('TTWO', 'TTWO'), ('TWTR', 'TWTR'), ('TXN', 'TXN'), ('TXT', 'TXT'), ('TYL', 'TYL'), ('UA', 'UA'), ('UAA', 'UAA'), ('UAL', 'UAL'), ('UDR', 'UDR'), ('UHS', 'UHS'), ('ULTA', 'ULTA'), ('UNH', 'UNH'), ('UNP', 'UNP'), ('UPS', 'UPS'), ('URI', 'URI'), ('USB', 'USB'), ('V', 'V'), ('VFC', 'VFC'), ('VIAC', 'VIAC'), ('VLO', 'VLO'), ('VMC', 'VMC'), ('VNO', 'VNO'), ('VRSK', 'VRSK'), ('VRSN', 'VRSN'), ('VRTX', 'VRTX'), ('VTR', 'VTR'), ('VTRS', 'VTRS'), ('VZ', 'VZ'), ('WAB', 'WAB'), ('WAT', 'WAT'), ('WBA', 'WBA'), ('WDC', 'WDC'), ('WEC', 'WEC'), ('WELL', 'WELL'), ('WFC', 'WFC'), ('WHR', 'WHR'), ('WM', 'WM'), ('WMB', 'WMB'), ('WMT', 'WMT'), ('WRB', 'WRB'), ('WRK', 'WRK'), ('WST', 'WST'), ('WTW', 'WTW'), ('WY', 'WY'), ('WYNN', 'WYNN'), ('XEL', 'XEL'), ('XLNX', 'XLNX'), ('XOM', 'XOM'), ('XRAY', 'XRAY'), ('XYL', 'XYL'), ('YUM', 'YUM'), ('ZBH', 'ZBH'), ('ZBRA', 'ZBRA'), ('ZION', 'ZION'), ('ZTS', 'ZTS')], max_length=200, null=True)),
                ('buy_sell', models.CharField(blank=True, choices=[('+', 'Kupno'), ('-', 'Sprzedaz')], max_length=8, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('hour', models.TimeField(blank=True, null=True)),
                ('shares_number', models.DecimalField(blank=True, decimal_places=8, default=0, max_digits=999, null=True)),
                ('course', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=999, null=True)),
                ('fare', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=999, null=True)),
                ('portfolio_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='optifolio.portfolio')),
                ('user_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='optifolio.customer')),
            ],
        ),
    ]
