from openai import OpenAI
import json
client = OpenAI(api_key="0",base_url="http://0.0.0.0:8000/v1")

def get_response(prompt):
    request = {
<<<<<<< HEAD
<<<<<<< HEAD
        "model": "bidding_outputs/finetune_outputs/qwen_pretrain_finetune_241230",
=======
        "model": "/home/lt_08321/ssd/wangweihang/LLaMA-Factory/outputs/saves/241216/qwen2.5-14b/full/pt",
>>>>>>> ad1c2617 (bidding)
=======
        "model": "bidding_outputs/finetune_outputs/bidding_pretrain_finetune_250118",
>>>>>>> 2e28cce4 (remote)
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ], 
        "max_tokens": 10000,
    }
    result = client.chat.completions.create(**request)
    return result.choices[0].message.content
    
    
prompts = [
    "有一个工程名称为“南通市东台管道联网供水（海安段）工程施工三标段（305）”的项目，项目分类：市政/管道，项目性质：新建,建设规模：“海安段给水管道工程长度约39.6千米。从如皋段接出，沿农田及村道向东北方向，在隆吉线位置穿越G204,并沿204国道向北至海安东台界。敷设DN2000管道长度约4.8千米，DN1800管道长度约34.8千米”，招标范围：“本项目共分三个标段。三标段为海安段给水管道工程305，管线全长总计约为12.4km：海安隆政泵站至白甸连接线分水点段，管线全长约12.4km,管径为DN1800单管,管线工程埋管段管材主要采用球墨铸铁管，顶管段、过障碍等部分特殊管段管材采用钢管”，方案分类：施工方案/管道/顶管。目前需要写顶管采用直径DN1800的钢管，长度为700米，管道深度为13米。顶管工作井和接收井长宽均为7*8m,采用沉井法制作。顶管机械采用适合管道直径的泥水平衡顶管机。施工内容包括顶管工作井/接收井的施工、顶管机械安装、管道顶进、钢管焊接、管道纠偏、管道注浆、长距离顶管通风、照明措施等，字数3000字左右，请你进行写作",
    "有一个工程名称为“南通市应急医院（公共卫生临床医学中心）配套道路工程”的项目，项目分类：市政/道路，项目性质：新建,建设规模：“一个标段，南通市应急医院（公共卫生临床医学中心）西侧路、北侧路及南侧路，道路全长约1100米，北侧路规划宽度18米，西侧路、南侧路规划宽度20米。设计等级为城市支路，设计时速20km/h”，招标范围：“施工图所示的南通市应急医院（公共卫生临床医学中心）配套道路工程，主要包括道路、桥梁、排水、管线、交通设施、绿化、土方等内容”，方案分类：施工方案/道路/沥青路面。目前需要写南通市应急医院周边道路全长997m,红线宽度18m，双向两车道，等级为城市支路，设计速度20km/h。道路横断面布置为3m（人行道）+12m（车行道）+3m（人行道）。包括软基处理、沥青路面铺设、新老路面搭接等，字数3000字左右，请你进行写作",
    "有一个工程名称为“嘉兴市市区快速路环线工程（三期二阶段）景观绿化工程”的项目，项目分类：市政/景观绿化，项目性质：新建,建设规模：“嘉兴市市区快速路环线工程（三期二阶段）起于中环北路城东路口，经过市区东部楔形绿地后，沿三环东路往南至广益路口,并与环线一期贯通，长约7.6公里（含广益路以南约500米）；地面辅道（三环东路公铁立交南侧至广益路）长约5.1公里，同步实施茶园路约350米”，招标范围：“嘉兴市市区快速路环线工程（三期二阶段）景观绿化工程施工实施范围为：高架主线（K21+345-K28+489.641，K0+000-K0+505，长约7.6km）、地面辅道(K23+475-K28+552，长约5.1km）景观绿化及茶园路等绿化恢复施工，包括三期二阶段施工图范围内的行道树、侧分带、中分带景观绿化，高架花箱景观绿化、绿化灌溉、景观亮化等景观绿化施工相关内容，一二期新增声屏障范围内的花箱拆除约8000米，具体详见工程量清单及图纸”，方案分类：施工方案/园林景观/景观绿化。目前需要写市区快速环线三期二阶段长约7.6km,包含高架花箱、道路行道树、中分带、侧分带的绿化，字数3000字左右，请你进行写作",
    "有一个工程名称为“杭州市三墩单元XH010201-17地块居住区养老院”的项目，项目分类：房建，项目性质：新建,建设规模：“建居住区养老院，主要建设内容包括生活用房、文娱与健身用房、康复与医疗用房、管理服务用房、残疾人之家、配套附属用房、地下车库、绿化工程等。总建筑面积约11337平方米，地上建筑面积8837平方米，地下建筑面积2500平方米”，招标范围：“招标文件、施工图及工程量清单范围内的内容。包括但不限于：1）发包人提供的全套施工图、修改图、图纸会审、工程指令、设计变更等范围内的基坑围护、地基与基础工程、结构工程、建筑工程、公共部位精装修工程、给排水工程、电气工程、通风工程、消防工程、智能化工程、电梯工程、泛光照明、室外市政配套工程、园林景观、铺装工程、空调工程、标识标牌、抗震支架、BIM等”，方案分类：施工方案/基础/土方。目前需要写土方开挖深度为3.6米，基坑长100米，宽50米，土方量为18000万方，采用放坡+土钉墙支护方式。基坑开挖施工方案，包含土方开挖，降排水，基坑回填，字数2500字左右，请你进行写作",
    "有一个工程名称为“四堡七堡单元JG1402-A2-82地块文化中心项目”的项目，项目分类：房建，项目性质：新建,建设规模：“总建筑面积22438平方米，其中地上建筑面积9288平方米，地下建筑面积13150平方米”，招标范围：“本次招标范围包括但不限于施工图范围内的基坑围护、桩基、土石方、土建、钢结构、装饰装修、幕墙、门窗、安装（给排水、电气、消防、暖通、弱电智能化）、防火门、电梯设备采购及安装、人防工程（包含标识标牌）、交通标识标线、地坪漆、室外给排水等。具体详见施工图审图纸、招标文件、工程量清单及发包人明确指令要求完成的其他工作。本次招标建安工程造价17447.7564万元”，方案分类：施工方案/主体/模板。目前需要写模板工程方案，搭设高度为7米，采用盘扣式支模架，最大梁长度9米，最大梁高0.5米，建筑总高度60米，总层数16层，字数2000字左右，请你进行写作",
    "有一个工程名称为“杭州市公安局交警支队车辆管理所建设工程”的项目，项目分类：房建，项目性质：新建,建设规模：“本项目总建筑面积约37269平方米，地上建筑面积26777平方米（其中新建建筑面积约19022平方米，保留建筑面积约7755平方米），地上7层；地下建筑面积10492平方米（其中新建建筑面积约8000平方米，保留建筑面积约2492平方米），地下1层，共分3幢单体建筑，总用地面积32265平方米”，招标范围：“本项目总建筑面积约37269平方米，地上建筑面积26777平方米，地下建筑面积10492平方米，招标范围为施工图范围内的土建工程、装修工程、土石方工程、基坑围护工程、电气工程、给排水工程、消防工程、幕墙工程、暖通工程、弱电工程、室外工程等（具体内容以提供的施工图及工程量清单为准）”，方案分类：施工方案/装饰/天棚。目前需要写天棚施工方案，包含轻钢龙骨纸面石膏板，吊杆长度1.2米，面积约4000平米，层高为4.2米，字数1500字左右，请你进行写作",
    "有一个工程名称为“科创走廊项目(一期)建设工程施工”的项目，项目分类：房建，项目性质：新建,建设规模：“总建筑面积约4.1万平方米，其中：地上建筑面积约3.2万平方米（研发中心、人才公寓及配套），地下建筑（一期地库）面积约0.9万平方米”，招标范围：“科创走廊项目（一期）建设工程施工，主要内容为2#研发中心、3#研发中心、4#人才公寓及地库土建、安装等工程施工”，方案分类：施工方案/主体/主体。目前需要写关于高度为8m，梁截面尺寸为500*1200的超过一定规模的危险性较大的分部分项工程方案，字数1000字左右，请你进行写作",
    "有一个工程名称为“广州市荔湾区西塱项目”的项目，项目分类：房建，项目性质：新建,建设规模：“项目规划总建筑面积约14.4万平方米。其中可售住宅面积约9.38万平方米，配套建筑面积约1.15万平方米；地下室面积约3.62万平方米，地下车库1-2层。建设内容包括小区住宅（高度大于50m，不超过100m）、配套幼儿园、社区卫生服务中心、地下车库（兼做人防）、垃圾站、室外景观、围墙等内容”，招标范围：“本次招标范围包括但不限于施工图范围内的基坑围护、桩基、土石方、土建、钢结构、装饰装修、幕墙、门窗、安装（给排水、电气、消防、暖通、弱电智能化）、防火门、电梯设备采购及安装、人防工程（包含标识标牌）、交通标识标线、地坪漆、室外给排水等”，方案分类：施工方案/屋面/屋面。目前需要写屋面施工方案，屋面有保温层、地砖面层，字数1000字左右，请你进行写作",
    "有一个工程名称为“瑞安市图书馆新馆建设工程—装修工程”的项目，项目分类：装饰装修，项目性质：装饰装修,建设规模：“总用地面积为36972.21㎡，总建筑面积60000㎡;地上建筑面积40000㎡（包括大厅及阶梯阅览区3618㎡，公共活动和展示区11615㎡,文献借阅服务区12285㎡,儿童阅览服务区6751㎡,培训区2254㎡,管理用房区1412㎡,设备用房2065㎡）;地下建筑面积20000㎡（包括自控书库区1973㎡,文献分拣区551㎡,业务管理区1031㎡,音乐活动区448㎡,餐厅及厨房区1944㎡,设备用房及车库14053㎡）；建筑高度23.95m”，招标范围：“装修(含空调系统、泛光照明、电动遮阳帘等)专业，具体以工程量清单及施工图纸为准”，方案分类：施工方案/装饰/墙面。目前需要写轻钢龙骨纸面石膏板墙面方案，字数1500字左右，请你进行写作",
    "有一个工程名称为“陕西省西咸新区沣东新城沣明路（原昆明路西延伸）高架段（阿房宫收费站-沣东界）市政项目EPC总承包项目”的项目，项目分类：市政/道路，项目性质：新建,建设规模：“沣东新城沣明路（原昆明路西延伸）高架段（阿房宫收费站-沣东界）市政项目EPC总承包项目西起新西宝高速阿房宫收费站（不含收费站广场），在收费广场东侧起高架，在避让地铁5号线地下结构的同时，向东连续跨越广场东环路、经三路、和平路、天台路、西户铁路后接地，以地面式快速路顺接西三环石桥互通，规划道路等级为城市快速路，规划红线标准段宽度为70m，阿房宫收费站处规划红线展宽至240m（中间收费站广场宽155m，两侧道路红线宽85m）。主线高架为M线与地面辅道为MD线，路线共线且长度均为2800m，主线高架设计速度为80km/h，高架标准段宽度25m，地面辅道设计速度为40km/h，地面辅道宽度50m~78m；昆左快速接线桥（接地点至合流点）路线长747.055m，设计速度80km/h，单向三车道，道路宽12.75m；昆右快速接线桥（接地点至合流点）路线长747.122m，设计速度80km/h，单向三车道，道路宽12.75m。昆左线地面道路长620.819m，设计速度40km/h，道路红线宽34.25m；昆右线地面道路长621.318m，设计速度40km/h，道路红线宽43.25m”，招标范围：“本次沣东新城沣明路（原昆明路西延伸）高架段（阿房宫收费站-沣东界）市政项目EPC总承包项目研究范围西起西宝高速高速阿房宫立交，向东沿老路至西三环石桥互通西侧沣东行政界线，全长约3.2km，施工图设计内容包含道路工程、桥梁工程、管线工程、交通及安全设施工程、照明工程、景观工程等主要专业”，方案分类：保证措施/组织/交通疏导。目前需要写市政工程交通疏导方案，字数2000字左右，请你进行写作",
    "有一个工程名称为“温岭经济开发区南区DB090307地块配套道路市政工程”的项目，项目分类：市政/道路，项目性质：新建,建设规模：“本项目总用地面积21587平方米，拟新建道路长约1300米，道路红线宽16米，建设内容包括：道路工程、排水工程、绿化工程、照明工程等”，招标范围：“施工图范围内招标人指定的道路、标志标线、排水排污、绿化、室外亮化等工程”，方案分类：施工方案/道路/标志标线。目前需要写市政工程标志标线施工方案，字数1000字左右，请你进行写作",
    "有一个工程名称为“浙江省高端化学品技术创新中心基建项目供配电工程”的项目，项目分类：市政/配电，项目性质：新建,建设规模：“本项目设有变压器总安装容量19700KVA，1个10KV总高配和4个变电所。供电电压等级10kV，电源引自环网室，电源电缆从环网室引入设在一层的总高配室”，招标范围：“设计图纸范围内的高低压开关柜、高压电缆、变压器、直流屏、电缆孔封堵、防火封堵、绝缘胶垫、配电屏蔽、模拟图板、变压器减震等项目（满足供电公司标准化验收要求）；供电线路及变电站和开闭所设备材料供应及施工；从总高配到各个变电所的所有供配电设施；计量柜的供应与安装；电表箱的供应；电表的安装（具体详见招标人提供的图纸、工程量清单）”，方案分类：施工方案/机电安装/配电柜。目前需要写配电柜安装施工方案，字数1500字左右，请你进行写作",
    "有一个工程名称为“温岭西站周边配套道路工程”的项目，项目分类：市政/道路，项目性质：新建,建设规模：“本项目主要建设内容包括：（1）规划六路：规划红线宽22.5m，道路全长456.86m；（2）九龙大道西延段：其中九龙大道西段规划红线45m，道路长度348.293m,九龙大道东东规划红线45m，道路长87.250m；（3）临时道路：临时道路红线宽17m，道路全长126.617m。由规划六路、九龙大道西段、九龙大道东段共同组成的中央环岛，建设地点：温岭市温峤镇内的温岭西站周边一带”，招标范围：“施工图范围内招标人指定的道路、桥接线、排水、标志标线、智能交通、通信预埋管、道路照明及绿化等工程。本次招标建安工程造价45363764元（不含渣土消纳费含税价2322616元；渣土消纳费不计入投标报价，但计入签约合同价）”，方案分类：施工方案/道路/排水。目前需要写排水工程施工方案，包含土石方施工、沟槽开挖与支护、沟槽基础施工、安管施工、检查井施工、闭水试验、沟槽回填等施工内容，字数6000字左右，请你进行写作",
    "有一个工程名称为“衢州市柯城区寺桥水库灌区工程”的项目，项目分类：水利/输配水，项目性质：新建,建设规模：“项目位于衢州市柯城区石梁镇、九华乡、万田乡、姜家山乡、沟溪乡、航埠镇、华墅乡等7个乡镇，灌溉范围东至庙源溪，西至大俱源，南至江山港，北至石梁镇坎底村。灌区设计灌溉面积8.04万亩，工程规模为中型，工程等别为III等。主要建设内容包括渠首工程、骨干输配水工程、骨干渠系建筑物、信息化工程及相关配套设施建设。渠首工程为杨家源水库新建塔式进水口一座、新建常山港泵站一座；骨干输配水工程为新建灌溉管网总长76.07千米，其中新建总干管0.23千米，新建东干管4.93千米，新建西干管5.29千米，新建西分干管6.04千米，新建南分干管22.97千米，新建西-1等4条支管及其分支管共23.76千米，新建其他田间放水管道12.83千米；骨干渠系建筑物为沿线新建阀井共338座，穿山穿路顶管26处共6451米，新建穿河倒虹吸6处；信息化工程为新增墒情、雨量、闸门远控各1处，视频监测点28处，阀门远控299处、压力监测125处、流量监测289处，建立1套支撑保障体系，新建寺桥水库灌区数字孪生平台，拓展柯城水网数据底板，构建寺桥水库灌区模型库”，招标范围：“衢州市柯城区寺桥水库灌区工程（主体配水工程）施工IV标段：东分支管部分，位于柯城区九华乡、万田乡和石梁镇，东-1支管范围从九华乡下坦村至慈张村；东-1-1支管范围从九华乡西珑口村至万田乡坞石村；东-2支管范围从九华乡至万田乡妙岭冈村。主要建设内容有：敷设东-1支管长7.77km、沿线放水口管道长1.17km；东-1-1支管长3.46km、沿线放水口管道长3.25km；东-2支管长3.74km、沿线放水口管道长0.38km，建设（安装）沿线蝶阀、空气阀等阀门（井）以及穿河、穿山等建筑物。工程所需钢管、球墨铸铁管、PE管和管道弯头、三通、盘承、盘插、异径管、法兰套、伸缩节、法兰等配件以及调流调压阀、蝶阀、空气阀、排泥阀等阀门和流量计、压力计、太阳能、电气控制箱、远程控制模块均为甲供，具体详见招标人提供的图纸及工程量清单。相应概算投资约3000万元，计划工期215日历天”，方案分类：施工方案/水利/给水。目前需要写给水工程施工方案，包含土石方施工、沟槽开挖与支护、沟槽基础施工、安管施工、管道防腐施工、阀门井施工、水压试验、管道附件及配件施工、沟槽回填等施工内容，字数6000字左右，请你进行写作",
    "有一个工程名称为“金义自贸区数字经济产业园及基础设施配套工程—金港大道提升工程”的项目，项目分类：市政/道路，项目性质：改扩建,建设规模：“金义自贸区数字经济产业园及基础设施配套工程—金港大道提升工程，道路全长约1867米，红线宽度35米，道路拓宽宽度约15米，最大雨水管径为DN2200，工程总投资约8586.84万元（不含政策处理费），其中工程费用约4712.37万元，工程建设其他费约3624.37万元，工程预备费约250.1万元。建设内容包含道路工程、桥梁工程、给水工程、污水工程、管线工程、绿化工程、路灯工程及交通附属设施等其他工程”，招标范围：“施工图纸内的全部工作内容，详见工程量清单及施工图图纸，具体以招标人要求为准”，方案分类：施工方案/道路/道路。目前需要写道路工程施工方案，包含测量、土石方施工、路基施工、垫层施工、基层施工、面层施工以及人行道、侧平石、挡土墙等附属工程施工内容，字数10000字左右，请你进行写作",
    "有一个工程名称为“常熟理工学院长三角工业数字化赋能中心项目施工总承包”的项目，项目分类：房建，项目性质：新建,建设规模：“本项目新建建筑面积30006.46平方米，其中地上建筑面积25070.31平方米，地下建筑面积4936.15平方米”，招标范围：“包含土方工程、桩基工程、基坑围护工程、土建装饰工程、安装工程、幕墙工程、电梯工程、室外及配套工程等，详见招标文件说明及工程量清单”，方案分类：施工方案/基础/土方。目前需要写土方开挖施工方案，字数1000字左右，请你进行写作",
    "有一个工程名称为“诸暨智能视觉产业园双创基地项目”的项目，项目分类：房建，项目性质：新建,建设规模：“本项目投资估算73086万元，工程概算73005万元，其中建安工程造价约56482万元，建设规模：项目建设总用地面积：111814.6㎡，总建筑面积225560.39㎡。其中Ⅰ期项目用地面积84995.1㎡，建筑面积182807.21㎡，其中地上面积182611.08㎡，地下面积196.13㎡；Ⅱ期项目用地面积26819.5㎡，建筑面积42753.18㎡。建设地点：诸暨市北三环路以南，学院路以西”，招标范围：“施工图范围内的土建安装工程，包括土建工程（桩基、基坑围护、各单体建筑、结构、幕墙、装修等）；安装工程（给排水、消防、电气、空调工程、弱电、暖通、抗震支架、电梯等）；不包括场外工程等，具体详见施工图。本次招标建安工程造价：约44222.0163‬万元”，方案分类：施工方案/屋面/屋面。目前需要写屋面工程施工方案，字数1000字左右，请你进行写作",
    "有一个工程名称为“兴化市戴泽中学教学楼工程”的项目，项目分类：房建，项目性质：改扩建,建设规模：“新建一幢四层教学楼，建筑总面积约4211.16平方米，本项目总投资额1806.2万元”，招标范围：“土建、安装等图纸及工程量清单载明的内容”，方案分类：施工方案/主体/主体。目前需要写主体结构施工方案，字数1000字左右，请你进行写作",
    "有一个工程名称为“乐清市北白象镇石船村标准厂房建设项目”的项目，项目分类：房建，项目性质：新建,建设规模：“总建筑面积41864.4㎡（地上计容建筑面积39200.8㎡，地下不计容建筑面积2663.6㎡)，其中共分为1#生产车间、2#生产车间、3#生产车间、4#生产车间、连廊及消控值班室等”，招标范围：“土建、电气、消防、给排水但不包含室外道路、围墙、室外管网、电梯、智能化工程等，具体详见施工图纸及工程量清单”，方案分类：施工方案/主体/钢结构。目前需要写1~4#楼建筑之间存在结构连廊，连廊高度4m~20m不等，钢结构连廊施工方案，字数3000字左右，请你进行写作",
    "有一个工程名称为“曹江路科技创新综合体项目--曹江路科创基地地块建设工程”的项目，项目分类：房建，项目性质：新建,建设规模：“用地面积约24292方米，总建筑面积约77995.02平方米。地上建筑面积61414.93平方米【其中科研办公47206.86平方米，配套商业约13041.65平方米(其中旅馆约11715.38平方米，商业1326.27平方米)，消控71.39平方米，配电418.01平方米，物业用房186.46平方米，井道连廊490.56平方米】，地下室面积约16580.09平方米，新建3幢科创楼，1幢旅馆及配套地下室。四栋建筑均为装配式混凝土结构，装配率都不低于60%”，招标范围：“施工图设计范围内的土建安装场外等工程。主要土建【含桩基、基坑围护、地下室、主体、幕墙、装修、标志标线等】；安装【含给排水系统、消防通风工程、喷淋工程、强电系统、智能化工程、暖通空调工程、电梯工程、抗震支架、亮化工程、光伏、雨水回收系统等】；场外【景观、排水、绿化、道路、消防水管、照明及场外生活污水处理系统等】工程，但不包括图纸中标注为用户自理部分（具体详见招标清单及施工图纸）。具体范围及内容详见施工图纸及工程量清单”，方案分类：施工方案/主体/装配式。目前需要写2层及以上主要采用装配式叠合板、ALC隔墙，装配式工程施工方案，字数3000字左右，请你进行写作"
]

output = []
for i, p in enumerate(prompts):
    
    result_1 = get_response(p)
    result_2 = get_response(p)
    result_3 = get_response(p)
    
    temp = {
        'q': p,
        'a_1': result_1,
        'a_2': result_2,
        'a_3': result_3,
    }

    print(temp)
    
    output.append(temp)
    
<<<<<<< HEAD
<<<<<<< HEAD
    with open("finetune_output_241230.json", "w", encoding="utf8") as f:
=======
<<<<<<< HEAD
    with open("finetune_output_250105.json", "w", encoding="utf8") as f:
=======
    with open("cpt_output.json", "w", encoding="utf8") as f:
>>>>>>> ad1c2617 (bidding)
>>>>>>> 4e401cfd (merge)
=======
    with open("finetune_output_250125.json", "w", encoding="utf8") as f:
>>>>>>> 2e28cce4 (remote)
        json.dump(output, f, ensure_ascii=False)