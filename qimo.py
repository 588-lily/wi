import streamlit as st
import pandas as pd

page= st.sidebar.selectbox("选择页面",["项目介绍","专业数据分析","成绩预测"])
if page == "项目介绍":
    st.title("🎓学生成绩分析与预测系统")
    '----------------------'
    c1,c2=st.columns(2)
    with c1:
        
        st.subheader("📚项目概述")
        st.write("本项目是一个基于Streamlit的学生成绩分析平台，通过数据可视化和机器学习技术，帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。")
        st.markdown('#### 主要特点：')
        with st.container():
            features=[
                '数据可视化：多维度展示学生学业数据',
                '专业分析：按专业分类的详细统计分析',
                '智能预测：基于机器学习模型的成绩预测',
                '学习建议：根据预测结果提供个性化改进']
            for feat in features:
                st.markdown(f"**●{feat}**")
    with c2:
        import streamlit as st

        images= [
                 {'url':'https://github.com/588-lily/wi/raw/main/111.png',
                  'parm':'学生数据分析示意图'
                },
                 {'url':'https://github.com/588-lily/wi/raw/main/222.png',
                  'parm':'学生数据分析示意图'
                        }

        ]
        if 'ind' not in st.session_state:
            st.session_state['ind']=0

        def nextImg():
            st.session_state['ind']=(st.session_state['ind']+1) % len(images)
        st.image(images[st.session_state['ind']]['url'],caption=images[st.session_state['ind']]['parm'])
        def lastImg():
            st.session_state['ind']=(st.session_state['ind']-1) % len(images)
        col1,col2=st.columns(2)   
        with col2:
           st.button('下一张',on_click=nextImg,use_container_width=True)
        with col1:
           st.button('上一张',on_click=lastImg,use_container_width=True)
    '--------------------------------'
    with st.container():
        st.subheader("📚项目目标")
        col1,col2,col3=st.columns(3)

        with col1:
            st.markdown('##### 目标一：分析影响因素')
            st.write('●识别关键学习指标')
            st.write('●探索成绩相关因素')
            st.write('●提供数据支持决策')
        with col2:
            st.markdown("##### 目标二：可视化展示")
            st.write('●专业对比分析')
            st.write('●成绩趋势研究')
            st.write('●学习模式识别')
        with col3:
            st.markdown("##### 目标三：成绩预测")
            st.write('●高精度学习模型')
            st.write('●个性化预测')
            st.write('●及时干预预警')
    '---------------------------------'       
    with st.container():
        st.subheader('🛠技术架构')
        cols=st.columns(4)
        with cols[0]:
            frontend_framework=st.text_input("前端框架",value="⭐Streamlit")
            
        with cols[1]:
            data_processing=st.text_input("数据处理",value="⭐Pandas\⭐Numpy")
            
        with cols[2]:
            visualization=st.text_input("可视化",value="⭐Plotly\⭐Matplotlib")
            
        with cols[3]:
            machine_learn=st.text_input("机器学习",value="⭐Scikit-learn")
            
            
    

elif page == "专业数据分析":
    st.title("📊专业数据分析")
    '-----------------------'
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    df = pd.read_csv("student_data_adjusted_rounded.csv")
    numeric_cols = ["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率", "期末考试分数"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # 强制转为数值型，异常值设为NaN
    df = df.dropna(subset=["专业", "性别"])
    
    # 1. 页面基础配置
    st.set_page_config(page_title="学生数据可视化分析", layout="wide")
    st.subheader("1.各专业学生学习数据可视化分析")

    # 2. 读取并预处理CSV数据
    df = pd.read_csv("student_data_adjusted_rounded.csv")

    # 3. 分栏布局：左侧放图表，右侧放数据表格
    col_left, col_right = st.columns([0.7,0.3])  # 左右分栏，宽度占比1:1


    # ---------------------- 左侧：性别比例柱状图 ----------------------
    with col_left:
        st.markdown("##### 各专业性别比例")
        # 统计各专业男女数量
        gender_prof = df.groupby(["专业", "性别"]).size().unstack(fill_value=0)
        # 绘制堆叠柱状图（适配截图风格）
        st.bar_chart(gender_prof, use_container_width=True, color=["#4285F4", "#EA4335"])  # 蓝-女，红-男


    # ---------------------- 右侧：性别比例数据表格 ----------------------
    with col_right:
        st.markdown("##### 性别比例数据")
        # 计算各专业男女占比（转为百分比）
        gender_ratio = df.groupby("专业")["性别"].value_counts(normalize=True).unstack(fill_value=0) * 100
        gender_ratio = gender_ratio.round(1)  # 保留1位小数
        # 显示表格（适配截图的“女/男”列）
        st.dataframe(
            gender_ratio,
            column_config={
                "女": st.column_config.NumberColumn(format="%.1f%%"),
                "男": st.column_config.NumberColumn(format="%.1f%%")
            },
            use_container_width=True
        )
    '------------------------------------'


    # ---------------------- 模块2：各专业学习指标对比（分组柱状图） ----------------------
    with st.container():
        st.subheader("2. 各专业核心学习指标对比")
        col_left, col_right = st.columns([0.7,0.3])
        # 计算各专业关键指标均值
        with col_left:
            prof_metrics = df.groupby("专业").agg({
                "每周学习时长（小时）": "mean",
                "上课出勤率": "mean",
                "期末考试分数": "mean"
            }).round(2)
            # 重置索引便于Plotly调用
            prof_metrics = prof_metrics.reset_index()
            # 数据重塑：将多指标转为长格式
            prof_metrics_melt = pd.melt(
                prof_metrics,
                id_vars="专业",
                value_vars=["每周学习时长（小时）", "上课出勤率", "期末考试分数"],
                var_name="指标类型",
                value_name="指标均值"
             )
            # 绘制分组柱状图
            fig_metrics = px.bar(
                prof_metrics_melt,
                x="专业",
                y="指标均值",
                color="指标类型",
                barmode="group",
                title="各专业学习指标均值对比（学习时长/出勤率/期末分数）",
                labels={"专业": "专业名称", "指标均值": "指标平均值"}
            )
            fig_metrics.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_metrics, use_container_width=True)
        with col_right:
            st.markdown("##### 详细数据")
            st.dataframe(prof_metrics,use_container_width=True)
    
        '--------------------------------------'


    # ---------------------- 模块3：各专业出勤率分布（彩色柱状图） ----------------------
    with st.container():
        st.subheader("3. 各专业上课出勤率分布")
        # 计算各专业出勤率均值（保留2位小数）
        col_left, col_right = st.columns([0.7,0.3])
        with col_left:
            attendance_prof = df.groupby("专业")["上课出勤率"].mean().round(3).reset_index()
            attendance_prof["上课出勤率"] = attendance_prof["上课出勤率"] * 100  # 转为百分比
            # 绘制彩色柱状图（按出勤率数值着色）
            fig_attendance = px.bar(
                attendance_prof,
                x="专业",
                y="上课出勤率",
                color="上课出勤率",
                color_continuous_scale=px.colors.sequential.Reds,
                title="各专业上课出勤率（%）",
                labels={"专业": "专业名称", "上课出勤率": "出勤率（%）"}
            )
            fig_attendance.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_attendance, use_container_width=True)
        with col_right:
            st.markdown("##### 出勤率排名")
            st.dataframe(attendance_prof,use_container_width=True)
    '-----------------------------------------'


    # ---------------------- 模块4：大数据管理专业专项分析（横向柱状图） ----------------------
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    st.subheader("4.大数据管理专业专项分析")
    # 顶部指标卡片
    bigdata_df = df[df["专业"] == "大数据管理"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("专业出勤率", f"{bigdata_df['上课出勤率'].mean()*100:.1f}%")
    with col2:
        st.metric("平均成绩", f"{(bigdata_df['期中考试分数']+bigdata_df['期末考试分数']).mean()/2:.1f}分")
    with col3:
        st.metric("作业完成率", f"{bigdata_df['作业完成率'].mean()*100:.1f}%")
    with col4:
        st.metric("平均每周学习时长", f"{bigdata_df['每周学习时长（小时）'].mean():.1f}小时")

    # 下方细分图表
    import numpy as np  # 导入numpy库，用于生成数据
    from scipy.stats import gaussian_kde  # 改用scipy的核密度函数
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
    # 1. 读取数据并筛选“大数据管理”专业
        df = pd.read_csv("student_data_adjusted_rounded.csv")
        bigdata_scores = df[df["专业"] == "大数据管理"]["期末考试分数"].dropna()  # 过滤空值

        # 2. 计算核密度（用scipy实现）
        kde = gaussian_kde(bigdata_scores)
        x_vals = np.linspace(bigdata_scores.min(), bigdata_scores.max(),100)  # 生成x轴取值
        y_vals = kde(x_vals)  # 计算对应密度

        # 3. 绘制直方图
        fig = px.histogram(
            x=bigdata_scores,
            nbins=10,
            histnorm="probability density",
            title="大数据管理专业期末成绩分布密度",
            labels={"x": "期末分数", "y": "分布密度"},
            opacity=0.7,
            color_discrete_sequence=["#2e8b57"]
        )

        # 4. 添加核密度曲线（用scipy计算的结果）
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name="核密度曲线1"
        ))

        # 5. 配置布局
        fig.update_layout(
            plot_bgcolor="white",
            xaxis_range=[0,100],
            xaxis_title="期末分数",
            yaxis_title="分布密度"
        )
        fig_box = px.box(
            bigdata_df, 
            y="期末考试分数", 
            title="大数据管理专业期末成绩分布", 
            color_discrete_sequence=["#2ecc71"],
            labels={"期末考试分数": "期末成绩（分）"}
        )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(fig_box, use_container_width=True)

else:
    import streamlit as st
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    import numpy as np

    st.set_page_config(page_title="🔮期末成绩预测", layout="wide", page_icon="📊")
    st.title("🔮期末成绩预测")
    st.markdown("---")
    df = pd.read_csv("student_data_adjusted_rounded.csv")


    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader('学号')
        student_id = st.selectbox("学号", df["学号"].unique())
        
        st.subheader('性别')
        gender = st.selectbox(
            '选择性别',
            ['男', '女'],
            label_visibility='collapsed'
        )
        
        st.subheader('专业')
        gender = st.selectbox(
            '请选择你的专业',
            ['工商管理', '人工智能','财务管理','电子商务','大数据管理'],
            label_visibility='collapsed'
        )
        
    
    with c2:
        # 2. 读取数据（替换为你的文件路径）
        df = pd.read_csv("student_data_adjusted_rounded.csv")

        # 3. 训练成绩预测模型（以学习时长、出勤率等为特征，预测期末成绩）
        def train_pred_model():
           # 选择特征列与目标列
            X = df[["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]]
            y = df["期末考试分数"]
            # 训练线性回归模型
            model = LinearRegression()
            model.fit(X, y)
            return model

        model = train_pred_model()

        # 4. 输入表单区域
        st.subheader("✨输入学生学习信息")
        with st.form("pred_form"):
            # 输入特征（支持手动修改）
            import streamlit as st
            from datetime import datetime, time
            hours = st.slider(
                '每周学习时长（小时）',
                10, 100,
                key="hours"
                )
            attendance = st.slider(
                '上课出勤率',
                0.6, 1.0,
                key="attendance"
                )
            mid_score = st.slider(
                '期中考试分数',
                40, 100,
                key="mid_score"
                )
            homework_rate = st.slider(
                '作业完成率',
                0.5, 1.0,
                key="homework_rate"
                )
            submit_btn=st.form_submit_button("提交预测")
            if submit_btn:
                input_data=[[hours,attendance,mid_score,homework_rate]]
                pred_score=model.predict(input_data)
                pred_score=max(0, min(100, pred_score))
                st.write(f"预测期末成绩{pred_score}")  

            
    
    st.markdown("---")
    if submit_btn:
        # 构造输入特征
        input_features = np.array([[hours, attendance, mid_score, homework_rate]])
        # 模型预测
        try:
            pred_score=model.predict(input_features)[0].round(2)
        except Exception as e:
            st.error(f"预测失败：{str(e)}")
            score=0
        
        st.subheader("预测结果")
        st.success(f"预测期末成绩：{pred_score}分")
    
        # 显示祝贺图（成绩达标时）
        if pred_score >= 80:
            st.image("https://github.com/588-lily/wi/raw/main/congratulations.jpg", use_container_width=True)  # 替换为你的烟花图路径
            st.markdown("**学习建议：保持当前状态，继续巩固知识！**")
        elif pred_score < 60:
            st.image("https://github.com/588-lily/wi/raw/main/cheers.jpg", use_container_width=True)  
            st.markdown("**学习建议：继续加油，不要气馁！**")
        else:
            st.warning("建议增加学习时长，提升课堂参与度~")
    
















    
