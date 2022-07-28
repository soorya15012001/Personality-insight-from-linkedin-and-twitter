import pandas as pd
import datetime

x = [
{'name': 'Rekha M Menon', 'text': 'chairperson senior managing director accenture india rekha menon chairperson senior managing director accenture india leading industry voice advanced technology led innovation socio economic progress rekha member executive council nasscom chairperson also member national council cii usibc india advisory council chair governing council national skill development corporation nsdc sector skill council board nasscom foundation data security council india dsci invest india board governor alma mater xlri school business two profit pratham book akshara foundation rekha regularly feature list powerful woman business india recognized among top lgbt ally executive globally prior joining accenture rekha entrepreneur founded two technology company profit active hiking cycling enthusiast rekha also voracious reader life bangalore india', 'single': 'C-ESTP'},

{'name': 'Anuj Trehan', 'text': 'cloud first executive global leader strategic partnership corporate venture capital intrapreneur business development strategy professional decade experience incubating scaling digital initiative fortune company e commerce startup specialty cloud enterprise tech partnership startup investment new business building product management analytics current global lead cloud first partnership accenture venture leader global technology business atci involves building scalable business high growth partner driving strategic capital investment disruptive startup cvc regular speaker premier b school industry conference passion technology incubating new business sport multiple medal football state college level education mba iim bangalore information technology pesit bangalore scaling strategic partnership key area like hybrid cloud edge infrastructure engineering industry cloud focus accelerating organic growth scaling innovation firm accenture venture leader global technology business atci deliver innovation inorganic organic growth multi billion dollar accenture tech practice responsible tech business development area like cloud devops microsoft amazon google salesforce ecosystem lead strategy innovation roadmap accenture new business focus scaling gtm play hi potential startup conceptualized scaled accenture global startup innovation lab focused innovation fortune client deep tech startup part strategy operation leadership team led sale strategy strategic project hpe group server storage networking business unit rated one year full time mba program india financial time mba general management focus strategy marketing entrepreneurship ceo iim bangalore first digital summit president sale marketing club led marketing team played key role delivering triple digit growth rate positioning hubzu com one industry leader online foreclosure home market usa liaised worldwide digital medium agency develop execute strategy digital marketing channel developed strategic partnership gtm new product initiative hubzu one fastest growing real estate ecommerce company proud member altisource family company altisource impressive track record residential real estate well mortgage financial service omnichannel interactive messaging initiative collaborated multi disciplinary team located globally deliver real time personalized consistent customer experience across channel leveraged predictive analytics technique behavioral targeting product recommendation deliver multi million dollar incremental revenue managed direct marketing campaign ranging cross sell high value promotional service mailing multiple business line fidelity investment', 'single': 'Ci-INFJ'},

{'name': 'Tina Philip', 'text': 'accenture venture open innovation management professional year experience information technology mobile automation industry emerging market proven track record end end planning design execution strategic project adept working multi cultural team across geography large corporation well start company led market development insight practice ibm bpo business growth market covered asia pacific central eastern europe middle east africa latin america completed project related market analysis competitive intelligence market segmentation new client acquisition customer need assessment served single point contact market insight project also supported ongoing deal founded elevate learning lab start mobile application development training industry led marketing effort shaped overall strategy handled day day operation established relation corporate customer well educational institution interfaced marketing strategy leadership team ibm global process service gps division growth market unit gmu identify key business priority designed budgeted managed several strategic project aimed achieving business goal gps business delivered fact based integrated insight actionable recommendation accelerate growth ibm gps emerging market cee mea la served single point contact market insight project query gps growth market', 'single': 'C-INFJ'},

{'name': 'Raghavan Iyer', 'text': 'senior managing director accenture raghavan iyer senior managing director accenture technology intelligent platform service lead advanced technology center accenture one largest important growth area accenture includes key platform microsoft adobe sap oracle salesforce workday raghavan also innovation lead across accenture advanced technology center pioneered culture innovation across organization also responsible flagship employee experience program across india successfully led accenture microsoft effort jointly achieve guinness world record title number microsoft cloud certification established business leader strong technology visionary raghavan steered several industry business group accenture two decade raghavan focus innovation process orientation people centricity technology thought leadership placed helm large scale organizational strategic initiative program myxperience myinnovation woman tech keynote speaker several forum including confederation indian industry raghavan held application outsourcing leadership role accenture industry group health public service product life science overall year experience around year u raghavan accenture executive sponsor entrepreneurship development institute india led organization wide program inclusion diversity woman tech leadership among corporate citizenship activity raghavan hold bachelor degree computer engineering university mumbai certified cloud advisor carnegie mellon university also hold certification including pmp six sigma greenbelt design six sigma', 'single': 'D-ESTP'},

{'name': 'Manisha Bhattacharya', 'text': 'managing director sale enablement manisha lead sale enablement accenture india intelligent platform service group supporting growth defining strategy driving opportunity origination harnessing best talent data intelligence passionate creating managing inclusive collaborative diverse ecosystem managing growing sale enablement team atc location function aligned internal sale process function largely include proposal authoring bid management research account opportunity based industry new market penetration competitive analysis marketing content development management sale operation leading passionate team sale enablement professional research content creative sale mobilization committed generating opportunity new microsoft platform across spectrum offering service focus digital transformation sale effectiveness working global leadership driving strategic leadership development executive talent management agenda across global delivery center one accenture key business unit includes facilitating talent calibration leadership assessment succession planning executive talent strategic core role across global center program managing leadership development initiative high potential cadre led client service sale enablement organization key vertical india delivery center created managed high performing team organizes executes offshore visit client potential client impacting business opportunity running several million dollar grew vertical dedicated proposal team tenure delivered significant saving offshoring proposal service function led large team associate setting efficient process place delivering well crafted proposal content high value opportunity led program management portfolio key high value client included demand supply fulfillment roster management capacity planning expansion client management led service management team tracking reporting critical sla compliance metric account champion people engagement sponsor csr lead business operation organization within life science vertical managed communication marketing event training metric operation csr within industry cell key focus employee engagement score monitoring people issue developmental plan creation industry training program business analyst center excellence participating planned employee interaction mean keeping informed engaged lead client service organization life science industry cell key function include managing dcso process demand supply management managing client visit delivery centre managing high value rfp rfi submission addition program managed key event created sale collateral conceptualised planned executed marketing event', 'single': 'Dc-ESTP'},

{'name': 'Tony Simon', 'text': 'technology community operation engineer enthusiastic problem solving via community engagement prefers move foster huge interest linking people place idea interest technology community management product process optimization user understanding pedagogy travel assisted prof santhosh venkatesh visiting faculty university pennsylvania course statistic problem solving batch young india fellow mission make learning relevant accessible aid technology world best practice creating exciting stuff school student want provide kid optimal learning experience enable teacher right aid providing clarity parent help steer kid future entrepreneur first brings together world ambitious people build startup scratch london berlin singapore hong kong bangalore part month program help individual form team develop idea raise funding investor order build world important company managed product portfolio eu market lead project new product development strategized maximisation eu profit via licensing strategy site transfer vendor renegotiations implemented organizational level metric milestone assessment sale operation team designed automated inventory replenishment logic front end unit u australia india analyzed product portfolio africa restructured manufacturing unit distribution channel', 'single': 'SC-ESFP'},

{'name': 'Akanksha R.', 'text': 'venture accenture corporate strategy post merger integration corporate development strategic initiative digital transformation product strategy corporate strategy professional currently working accenture venture arm stint accenture spent year infosys working across corporate strategy post merger integration corporate innovation ecosystem development product management infosys lab consulting program lead corporate strategy infosys key role lead manage acquisition post merger integration digital target delivering deal value value creation inorganic strategy primary responsibility day day work involves strategic planning tracking integration activity performing due diligence managing defining tracking synergy stakeholder consensus management acquired entity among many others goal make sure integration better last ensure achieve strategic goal planned integration successfully previously worked corporate innovation function involved startup ecosystem across globe well responsible gtm revenue product road mapping internal ai data automation product lead startup relation managed startup ecosystem infosys innovation network iin fintech ai cloud quantum computing cybersecurity worldwide shipped product client across globe corporate innovation role brief stint consulting part innovation partner program infosys worked innovation emerging tech consultant role analyze customer landscape advise innovation strategy started career business analyst working major u bank consumer wealth management domain lead business analyst data analytics insight technology space open interesting challenging eclectic opportunity accenture venture open innovation innovation strategy venture acquisition strategy merger acquisition growth strategy startup ecosystem', 'single': 'D-ESTP'},

{'name': 'MINA JEEVAN', 'text': 'innovation ecosystem associate principal accenture venture product management party integration mobile payment reaching woman techpreneurs indian ecosystem please use link apply accenture woman founder program congrats anoop n team great initiative look forward see amazing startup emerge innovation team time year accenture venture back another exciting edition flagship event edition accenture venture challenge powered microsoft x x identify innovative b b deeptech indian startup driving innovation never normal era accentureventures ecosystem digitalcommerce supplychainresilience systemresilience responsibletech', 'single': 'CI-ESTJ'},

{'name': 'Balaji Sridharan', 'text': 'driving strategic partnership accenture venture highly accomplished dedicated professional industry leading certification extensive experience program project management involving stake holder interaction project planning estimation monitoring progress reporting project level issue resolution technology conflict resolution expectation risk management cross functional process team interaction coordination operational risk compliance business continuity planning reporting driving strategic eco system partnership planning scheduling delivery management deliverable concurrent project improving operation enhancing business growth setting infrastructure project management service delivery ability handle offshore onshore model responsible software development life cycle includes tracking project coordinating client requirement gathering technical functional specification data interface process design module interface development testing integration implementation cohesive team player fast learning curve along strong analytical problem solving innovation planning organizational communication interpersonal skill accenture venture driving gtm partnership growth stage b b startup across globe area metaverse enterprise data ai blockchain extended reality others bringing innovation onboarding new venture partner driving program management university collaboration iisc bangalore plugged venture solution building virtual experience center innovation hub driving intraprenuership program helping internal ceo scale idea leading industry x atcp leveraging venture solution client deal accenture venture challenge handling platform virtual event procurement legal lead accenture venture overall hub startup zone operation lead driving cloud migration project banking client kogentix amp automated machine learning platform technology delivers end end solution integrates wrangle data multiple source build machine learning model operationalizes ai application generate visible business result partner business stakeholder enterprise architecture software engineer se analysing requirement analysing impact proposing design fleshing detailed design finally driving design completion feature team ensures feature area deliver expected value customer business objective applies strategic understanding timing rationale design choice feature area engage business process unit work closely upstream downstream application owner effectively build trusted advisor relationship team consistent time budget delivery portfolio point contact within verizon enterprise solution infrastructure project management responsibility included implementation enterprise level program cloud migration data center migration tech refresh existing hardware providing cloud consultation various technology team facilitate smooth migration monitoring managing ordering provisioning new hardware software end end management new request within portfolio handling budgetary management hardware project management inter organizational communication collaboration data collection collective status reporting open request effort facilitating multiple project across business group solution center geography efficient project management coordination project operation related product lifecycle management plm enterprise project management epm alm house tool test management tool etc running multiple cloud migration project across domain initiation planning execution monitoring control closure project executing project charter plan milestone execute monitor project within triple constraint negotiating customer business owner related sow requirement planning timeline delivery meet customer expectation following stage project per pmp itil standard assisting manager efficient management project dashboard kpi reporting knowledge base prepare dashboard kpis related multiple project presenting relevant stakeholder proactively work risk management quality management driving meeting autonomously effectively project team business owner solution center management handling entire branch operation final checking validation new business proposal file follow new business issuance central operation underwriting team managing cpa team decision making per financial underwriting norm responsible maintaining file mi accordance audit requirement handling customer query complaint maintaining tat new business issuance customer service operation ensuring six sigma maintaining evaluating various mi regarding new business proposal referral case sampling case sample medical etc reporting top management handling bank related operation including cash cheque reconciliation eod handling pre post license issue advisor primary vault custodian etc part planning logistics team analyzed customer requirement forecasted based past requirement worked purchase team material procurement based requirement collaborated various team quality product delivery maintained optimum level inventory avoiding production line stoppage planned production according customer requirement controlled effective supply chain management logistics negotiated forwarders controlling freight cost ageing analysis invoice prepared weekly monthly production customer requirement report provided weekly shipping report customer daily updating customer requirement formulating minimum transit time import export tracking shipment daily basis updating customer regular basis part team developing activity based costing sub process', 'single': 'C-ESTP'},

{'name': 'Claire Suellentrop', 'text': 'saas marketing growth advisor described founder grace founder coo forget funnel boutique consulting firm help recurring revenue business go piecemeal marketing tactic repeatable scalable growth privileged work great company like sparktoro wistia fullstory sprout social appcues wildbit many forgetthefunnel com expert leveraging customer insight fuel revenue generating marketing program year experience marketing saas former director marketing hire calendly helped take company pre revenue first arr people ftf boutique consulting firm help recurring revenue business unlock best repeatable scalable path growth saas lifecycle email automation understands unique customer data model', 'single': 'SI-ESFJ'},

{'name': 'Ashish Kumar', 'text': 'innovation evangelist deeptech enthusiast venture industry strategy lead accenture xdeloitte strategist demonstrated experience growth strategy consulting deep tech venture ecosystem engagement accenture venture open innovation india innovation ecosystem strategist innovation asset development cloud intelligent platform industry bu venture interlock strategy startup open innovation ecosystem strategy venture partner gtm venture architecture advisory innovation strategy cyber portfolio growth ambition office advisory leadership portfolio rationalization strategic transformation program asset globalization apac portfolio hyperscale', 'single': 'DC-ESTJ'},

{'name': 'Kallan H', 'text': 'vice president head talent acquisition elevation capital executive search consultant leadership hiring highly referenced executive search professional proven recruiting expert complimented year experience partnered company hiring director cxo level position startup midsize multi billion conglomerate successfully delivered senior executive mandate consistently received high performance rating extensively partnered investor board director ceo founder technology leader head interested making connection prospective senior leader candidate would like know pursue executive level opportunity portfolio company across domain please link even dont need job staying network beneficial opportunity first check network current area focus elevation capital feel free contact kallan elevationcapital com currently building great team portfolio company hiring director cxo level position various company across domain job mostly filled private networking necessarily advertised elevation capital venture growth capital fund invested helping asia exceptional company grow concept ipo supporting visionary entrepreneur across diverse sector elevation capital founded currently manages billion management investment since inception india portfolio includes paytm dial makemytrip nse bookmyshow rivigo swiggy sharechat meesho acko cleartax urbanclap sector invest information technology internet mobile consumer product service healthcare education modern agriculture financial service industrials current area focus elevation capital idea beginning successful business build great team delivers amazing result currently hiring director cxo level position various portfolio company across domain technology product management strategy sale marketing finance operation etc job mostly filled private networking necessarily advertised feel free mail kallan elevationcapital com one initial member longhouse complimented significant experience executive search professional head hunter partnering candidate ceo head founder investor board director hiring various business critical senior leadership cxo director position start ups midsize multi billion conglomerate', 'single': 'I-ENTJ'},

{'name': 'Ratan Postwalla', 'text': 'partner founder people trust leadership coach career strategist people trust consultancy focused building capability maximising potential service offering targeted organisation individual assist organisation large small providing customised solution advisory learning build enhance human capital assist client prevailing business challenge across globe specifically enhanced virtual learning solution making easily adoptable scalable incrementally effective partner founder people trust lead people trust operation advisory practice also design delivers leadership behavioral program corporates university oversees business development client management teaching course strategic problem solving comprehensive performance management two year mba program business development client management performance management member finance transformation leadership team business development client management global banking insurance client based europe member finance transformation leadership team responsible performance management global team consultant independently managed assurance engagement client banking manufacturing technology sector', 'single': 'Ci-INFJ'},

{'name': 'Amit Ganeriwalla', 'text': 'senior partner mckinsey company senior partner mckinsey company lead global energy material sector india two decade experience management consulting served variety organization within energy material sector including family owned conglomerate large multinational corporation state owned enterprise area expertise lie end end transformation turning around business accelerating growth work ceo founder management team shape long term strategic agenda build new capability drive change passionate establishing new way working recent work focused helping company adopt leverage digital analytics capability scale published extensively global trend identifying effective strategy company developed emerging economy prior joining mckinsey served managing director senior partner boston consulting group held several global leadership role year distance runner avid reader political economic history', 'single': 'CS-ISTP'},

{'name': 'Neil Barman', 'text': 'chief growth officer board observer growth hacker storyteller early stage investor always hiring sale rockstars decade experience saas direct customer sale marketing process business leadership experience managing sale marketing account management function service product environment deep understanding building sale revenue generation function start ups scaling organisation across industry region apart leading growth function globally yellow ai one founding member sale enablement society india malaysia ambassador future sale apac community advisory board member multiple start ups india malaysia u mentor entrepreneurship cell bit pilani india spearheading growth function yellow messenger globally building sale customer success team diversify newer territory domain managing highly effective network channel patners ranging large si mid size seller network across region currently leading growth function team including sale account management inside sale partner management spearheading growth function yellow messenger globally building sale customer success team diversify newer territory domain managing highly effective network channel patners ranging large si mid size seller network across region currently leading growth function team including sale account management inside sale partner management sale enablement society s volunteer organization focused elevating role sale enablement organization worldwide engagement communication research development first non profit sale enablement community malaysia founded united state five founding member s grown member country chapter across globe member represent area sale enablement community practitioner supplier industry expert academic sale enablement society volunteer organization founded january diverse group like minded sale marketing professional based washington c area s overall mission identifies best practice successful outcome clarifies operation sale enablement business develops criterion sale enablement role within successful organization', 'single': 'I-INFJ'},

{'name': 'Avnish Sabharwal', 'text': 'digital innovation venture deeptech saas startup sustainability mentor angel investor innovator strategist technology evangelist year extensive experience track record around market making growth hacking corporate innovation digital transformation leadership development top fortune client mature emerging market successful track record building new practice service based organization inception making sustainable high performing business implementing strong management leadership best practice backed world class system process control current role accenture india responsible innovation designing leading open innovation programme india including collaborating start ups vcs accelerator incubator industry body like nasscom cii ficci investment acquisition building deal pipeline making strategic minority investment well identifying selecting potential acquisition acquihire target academia leading strategic collaboration leading university accenture iit iisc iim area relating sustainability cloud autonomous robotic system deal origination originating deal selected white space segment account focus digital innovation prior accenture worked ibm global business service india united kingdom almost decade various leadership role served indian armed force seven year performed role aide de camp governor madhya pradesh awarded top corporate innovator award specialty digital venture open innovation eco system architect investment funding sustainability exponential technology practice builder talent development responsible scaling accenture digital innovation capability india work extensively indian start ecosystem identify invest acquire leading edge digital technology platform iot ai ar big data cloud cyber security space also lead growth strategy accenture role involves defining growth innovation agenda profitability road map competitive positioning accenture india key focus area includes working global house centre gics captive major global client helping set run scale operation india well help transform digital innovation hub parent organisation led team plus consultant across asia pacific europe latin america responsible providing market insight help design growth strategy build financial model investment case needed accelerate ibm growth high growth business like smarter planet digital emerging market part high profile cross functional task force set ibm chairman responsible formulating long term strategy business planning ibm growth greater china led go market strategy including opportunity customer competitive analysis ibm entry sri lanka bangladesh instrumental building ibm offshore strategy consulting practice well captive knowledge process offshoring business including building analytics center excellence leadership team grew strategy consultant two half year team provided strategic knowledge advisory service ibm well top client globally support growth market entry strategy financial due diligence business model transformation industry company analysis cost profitability benchmarking served aide de camp adc head state madhya pradesh top indian army officer get nominated ministry defense position based demonstrated leadership quality sustained period time within indian armed force officer indian army performed number staff operational posting across country helped build world class combat honed expansive skill set strategic planning war gaming competitive intelligence leader development rigorous standard enforcement innovation execution', 'single': 'C-ESTP'},

{'name': 'Anand Deshpande', 'text': 'founder chairman persistent system talk india gratitude entrepreneurship lifeatpersistent persistentsystems focused helping individual become job creator really looking forward event invite join u may pune segment harish mehta book tour magnificent book maverick effect maverick effect story nasscom mehta twin harish dewang got competitor collaborate india best interest indian software industry owes success nasscom opportunity salute harish effort nasscom harish also responsible setting tie india thank shantha mohan sharing book inviting write foreword aspiring manager excellent book guide leadership journey leadership thankyou llwtb learn amisha patel ganesh natarajan also visit new office bridgewater new jersey somerset corporate boulevard suite bridgewater township usa love bhageerath office last six month worked revamp interior ready changing work habit really like way interior evolved may actually consider coming office often making habit quarter quarter growth fourth straight quarter qoq growth proud team persistent sandeep kalra sunil sapre keith landis dedicated member team persistent seebeyondriseabove q financialresults know patrick valduriez thirty plus year work important hard database problem thorough work want understand take scale transactional database cloud good paper read thanks patrick pointing work great meet two long time friend bay area want call anyone old wendy fong feyzi fatehi feyzi fatehi book really nice given good idea write book deasra foundation entrepreneurialjourney congratulation sameer bendre yogesh patgaonkar mcc welcome persistent thank moneshia eltz great meet mother delhi great learn making difference community hi mediaagility team welcome persistent system invitation close mumbai international airport csia great place catch last meeting take first meeting land seebeyondriseabove lifeatpersistent mumbai welcome thank anant maheshwari support look forward extending year relationship microsoft sandeep kalra keith landis seebeyondriseabove lifeatpersistent excited welcome rajiv korpal rahul bajaj data glove inc team persistent setting microsoft business unit acquisition strengthens thirty year relationship microsoft seebeyondriseabove lifeatpersistent welcometotheteam', 'single': 'DC-INFJ'},

{'name': 'Anuradha Nath', 'text': 'india technology cao morgan stanley coo chief staff role chair council project program management vendor governance business management previously senior manager experience wealth mgmt retail banking health insurance domain previously consultant director designation worked variety role across gwm mssb pwm india international wealth mgmt mumbai including management project program mgmt vendor governance business management series java specialist mainframe programmer system analyst worked primarily unisys mainframe consulted onsite scottish life assurance edinburgh month', 'single': 'CS-ESTJ'},

{'name': 'Ashish Tulsian', 'text': 'building posist making restaurant prosperous responsible sale strategy marketing product vision team building everyday fire fighting startup encounter brand development web site traffic growth web site advertising revenue developed brand strategy statistic system strategic consulting including business plan sale strategy development changing super excited posistturns posist praval singh said simple limited word guess holy grail remote office work way learn dive head first last year world took cognisance important addressing sexual harassment workplace posh also got added part compliance govt optional anymore welcomed step year back making sure implemented check box item compliance brought force education open dialogue team posist technology yesterday annual session esha shekhar took u do donts sensitizing u kind behaviour funny right way address objection voicing early voicing responsibly alot people lot question founder share doubt going growing different experience year year opportunity help question many grey area put perspective personally team discussing topic around posh hand format healthy empowering till far end hygiene hygiene major part building healthy culture live saurabh sengupta tonight setting international sale saas product excited excited looking forward marketing roundtable today marketer come join nikunj kewalramani sharing restaurant time journey looking forward learn fellow marketer enough inspiration silicon valley want emulate founder friendliness virtue almost still one toughest thing fund raise negotiating termsheet time win lose investor fairness virtue yet good founder take care much talking side today going live builder club discord congratulation arvind parthiban team superops ai kicked part journey prime report uae edition launching soon excited life post pandemic different differently accelerated restaurant restauranttechnology cloudkitchens posist hospitality excited chat anirudh today always inspired built artha venture partner far apart true embodiment founder friendly founder first also transparent pursuit thought check writing looking forward damanitalks excited looking forward posist mixer today conducting masterclass building running cloud kitchen tomorrow hellomeets excited posist cloudkitchens hellomeets darkkitchens ghostkitchens', 'single': 'CI-ESTJ'},

{'name': 'Basab Pradhan', 'text': 'non executive chairman coforge ltd board member provana responsible transformation company sale account management pursuit operation also oversaw marketing alliance large deal outsourcing group member executive council company authored book offshore india service juggernaut published penguin january offshore service industry attracts lot medium coverage little depth analysis book explores indian offshore service industry inside condition created juggernaut two decade keep growing rate big get challenge face future', 'single': 'D-ESFP'},



]

pd.DataFrame(x).to_csv("verify_linkedin.csv")