import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import json

# Load the data
file_path = 'CEOs - data .xlsx'  # Ensure the file path is correct
data = pd.read_excel(file_path)

# Load language-specific JSON file
language = st.selectbox('Select Language', ["English", "العربية"])

if language == "العربية":
    with open('ar.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
else:  # Assuming default to English
    with open('en.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)

def translate(key):
    return translations.get(key, key)

# Function to calculate the percentage chance of becoming a CEO
def calculate_ceo_chance(user_data, dataset):
    filtered_data = dataset.copy()
    for key, value in user_data.items():
        filtered_data = filtered_data[filtered_data[key] == value]
    total_ceos = len(dataset)
    match_ceos = len(filtered_data)
    chance = (match_ceos / total_ceos) * 100
    return chance

# Function to find the best scenario
def find_best_scenario(dataset):
    best_major = dataset['التخصص'].mode()[0]
    best_university = dataset['الجامعة'].mode()[0]
    best_graduation_country = dataset['دولة التخرج'].mode()[0]
    best_highest_qualification = dataset['آخر مؤهل'].mode()[0]
    best_years_before_appointment = dataset['السنوات قبل التعيين'].median()
    best_years_before_appointment_same_entity = dataset['السنوات قبل التعيين في نفس الجهة'].median()
    best_gender = dataset['النوع'].mode()[0]
    best_sector = dataset['القطاع'].mode()[0]
    best_first_ceo_appointment = dataset['اول تعيين له كرئيس تنفيذي؟'].mode()[0]
    best_first_organization = dataset['اول جهة يعمل بها'].mode()[0]
    best_longest_duration_organization = dataset['أطول مدة جهة يعمل بها'].mode()[0]

    best_scenario = {
        'التخصص': best_major,
        'الجامعة': best_university,
        'دولة التخرج': best_graduation_country,
        'آخر مؤهل': best_highest_qualification,
        'السنوات قبل التعيين': best_years_before_appointment,
        'السنوات قبل التعيين في نفس الجهة': best_years_before_appointment_same_entity,
        'النوع': best_gender,
        'القطاع': best_sector,
        'اول تعيين له كرئيس تنفيذي؟': best_first_ceo_appointment,
        'اول جهة يعمل بها': best_first_organization,
        'أطول مدة جهة يعمل بها': best_longest_duration_organization
    }

    return best_scenario

# Streamlit app title
st.title(translate("CEO Predictor"))

# Option menu for navigation
selected = option_menu(
    menu_title=None,
    options=[translate("Predictor"), translate("Best Scenario"), translate("Overview"), translate("Contact")],
    icons=["house", "graph-up", "bar-chart", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == translate("Predictor"):

    # User inputs
    user_data = {}
    user_data['التخصص'] = st.selectbox(translate('Major'), options=data['التخصص'].unique())
    user_data['الجامعة'] = st.selectbox(translate('University'), options=data['الجامعة'].unique())
    user_data['دولة التخرج'] = st.selectbox(translate('Graduation Country'), options=data['دولة التخرج'].unique())
    user_data['آخر مؤهل'] = st.selectbox(translate('Highest Qualification'), options=data['آخر مؤهل'].unique())
    user_data['السنوات قبل التعيين'] = st.slider(translate('Years Before Appointment'), min_value=0, max_value=50, value=int(data['السنوات قبل التعيين'].mean()))
    user_data['السنوات قبل التعيين في نفس الجهة'] = st.slider(translate('Years Before Appointment in the Same Entity'), min_value=0, max_value=50, value=int(data['السنوات قبل التعيين في نفس الجهة'].mean()))
    user_data['النوع'] = st.selectbox(translate('Organization Type'), options=data['النوع'].unique())
    user_data['القطاع'] = st.selectbox(translate('Sector'), options=list(data['القطاع'].unique()) + [translate('Others')])
    user_data['اول تعيين له كرئيس تنفيذي؟'] = st.selectbox(translate('First Appointment as CEO?'), options=data['اول تعيين له كرئيس تنفيذي؟'].unique())
    user_data['اول جهة يعمل بها'] = st.selectbox(translate('First Organization'), options=list(data['اول جهة يعمل بها'].unique()) + [translate('Others')])
    user_data['أطول مدة جهة يعمل بها'] = st.selectbox(translate('Longest Duration in an Organization'), options=data['أطول مدة جهة يعمل بها'].unique())

    # Calculate chance
    chance = calculate_ceo_chance(user_data, data)
    # Show the results in a donut chart (red)
    fig = px.pie(values=[chance, 100 - chance], names=[translate('Chance to be CEO'), translate('Others')], hole=.4, title=translate('Chance to be a CEO in the Future'))
    fig.update_traces(marker=dict(colors=['#FF6347', '#E5ECF6']))  # Red color for CEO chance
    st.plotly_chart(fig)

    # Provide insights in styled cards
    total_ceos = len(data)
    field_match = len(data[data['التخصص'] == user_data['التخصص']])
    country_match = len(data[data['دولة التخرج'] == user_data['دولة التخرج']])
    qualification_match = len(data[data['آخر مؤهل'] == user_data['آخر مؤهل']])
    years_before_appointment_match = len(data[data['السنوات قبل التعيين'] == user_data['السنوات قبل التعيين']])
    years_before_appointment_same_entity_match = len(data[data['السنوات قبل التعيين في نفس الجهة'] == user_data['السنوات قبل التعيين في نفس الجهة']])
    gender_match = len(data[data['النوع'] == user_data['النوع']])
    sector_match = len(data[data['القطاع'] == user_data['القطاع']])
    first_ceo_appointment_match = len(data[data['اول تعيين له كرئيس تنفيذي؟'] == user_data['اول تعيين له كرئيس تنفيذي؟']])
    first_organization_match = len(data[data['اول جهة يعمل بها'] == user_data['اول جهة يعمل بها']])
    longest_duration_organization_match = len(data[data['أطول مدة جهة يعمل بها'] == user_data['أطول مدة جهة يعمل بها']])

    
    st.write(f"### {translate('Insights')}")
    st.markdown("""
    <style>
        .insight-card {
            flex: 1;
            padding: 10px;
            margin: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            min-width: 200px;
            text-align: center;
        }
        .insight-card h3 {
            font-size: 20px;
        }
        .insight-card p {
            font-size: 16px;
            color: #FF6347; /* Red color for percentage values */
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap;">
        <div class="insight-card">
            <h3>{translate('Education Field')}</h3>
            <p>{field_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Graduation Country')}</h3>
            <p>{country_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Highest Qualification')}</h3>
            <p>{qualification_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Years Before Appointment')}</h3>
            <p>{years_before_appointment_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Years Before Appointment in the Same Entity')}</h3>
            <p>{years_before_appointment_same_entity_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Organization Type')}</h3>
            <p>{gender_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Sector')}</h3>
            <p>{sector_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('First Appointment as CEO?')}</h3>
            <p>{first_ceo_appointment_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('First Organization')}</h3>
            <p>{first_organization_match / total_ceos * 100:.2f}%</p>
        </div>
        <div class="insight-card">
            <h3>{translate('Longest Duration in an Organization')}</h3>
            <p>{longest_duration_organization_match / total_ceos * 100:.2f}%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif  selected == "Best Scenario" or selected == "أفضل سيناريو":
    
    best_scenario = find_best_scenario(data)

    st.markdown("""
    <style>
        .best-scenario-card {
            flex: 1;
            padding: 10px;
            margin: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            min-width: 200px;
            text-align: center;
        }
        .best-scenario-card h3 {
            font-size: 20px;
        }
        .best-scenario-card p {
            font-size: 16px;
            color: #FF6347; /* Red color for values */
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="best-scenario-card">
        <h3>{translate('Major')}</h3>
        <p>{best_scenario['التخصص']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('University')}</h3>
        <p>{best_scenario['الجامعة']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Graduation Country')}</h3>
        <p>{best_scenario['دولة التخرج']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Highest Qualification')}</h3>
        <p>{best_scenario['آخر مؤهل']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Years Before Appointment')}</h3>
        <p>{best_scenario['السنوات قبل التعيين']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Years Before Appointment in the Same Entity')}</h3>
        <p>{best_scenario['السنوات قبل التعيين في نفس الجهة']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Organization Type')}</h3>
        <p>{best_scenario['النوع']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Sector')}</h3>
        <p>{best_scenario['القطاع']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('First Appointment as CEO?')}</h3>
        <p>{best_scenario['اول تعيين له كرئيس تنفيذي؟']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('First Organization')}</h3>
        <p>{best_scenario['اول جهة يعمل بها']}</p>
    </div>
    <div class="best-scenario-card">
        <h3>{translate('Longest Duration in an Organization')}</h3>
        <p>{best_scenario['أطول مدة جهة يعمل بها']}</p>
    </div>
    """, unsafe_allow_html=True)

elif selected == "Overview" or selected == "نظرة عامة":
    st.write("### " + translate('Overview of CEO Data'))
    
    # Define the color to use for all histograms and pie chart
    color = '#FF6347'  # Red color
    
    st.write("#### " + translate('Distribution of Majors'))
    fig1 = px.histogram(data, y='التخصص', color_discrete_sequence=[color], histnorm='percent')
    fig1.update_yaxes(title=translate('Percentage'))
    fig1.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig1)
    
    st.write("#### " + translate('Distribution of Universities'))
    fig2 = px.histogram(data, y='الجامعة', color_discrete_sequence=[color], histnorm='percent')
    fig2.update_yaxes(title=translate('Percentage'))
    fig2.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig2)
    
    st.write("#### " + translate('Distribution of Graduation Countries'))
    fig3 = px.histogram(data, x='دولة التخرج', color_discrete_sequence=[color], histnorm='percent')
    fig3.update_yaxes(title=translate('Percentage'))
    fig3.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig3)
    
    st.write("#### " + translate('Distribution of Highest Qualifications'))
    fig4 = px.histogram(data, x='آخر مؤهل', color_discrete_sequence=[color], histnorm='percent')
    fig4.update_yaxes(title=translate('Percentage'))
    fig4.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig4)
    
    st.write("#### " + translate('Years Before Appointment'))
    fig5 = px.histogram(data, x='السنوات قبل التعيين', color_discrete_sequence=[color], histnorm='percent')
    fig5.update_yaxes(title=translate('Percentage'))
    fig5.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig5)
    
    st.write("#### " + translate('Years Before Appointment in the Same Entity'))
    fig6 = px.histogram(data, x='السنوات قبل التعيين في نفس الجهة', color_discrete_sequence=[color], histnorm='percent')
    fig6.update_yaxes(title=translate('Percentage'))
    fig6.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig6)
    
    st.write("#### " + translate('First Appointment as CEO?'))
    fig7 = px.pie(data, names='اول تعيين له كرئيس تنفيذي؟', hole=.4, color_discrete_sequence=[color, '#E5ECF6'])
    st.plotly_chart(fig7)

    st.write("#### " + translate('Distribution of Sectors'))
    fig_sector = px.histogram(data, y='القطاع', color_discrete_sequence=[color], histnorm='percent')
    fig_sector.update_yaxes(title=translate('Percentage'))
    fig_sector.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig_sector)

    st.write("#### " + translate('Distribution of Organization Type'))
    fig8 = px.pie(data, names='النوع', hole=.4, color_discrete_sequence=[color, '#E5ECF6'])
    st.plotly_chart(fig8)

    st.write("#### " + translate('Distribution of First Organization'))
    fig_first_org = px.histogram(data, y='اول جهة يعمل بها', color_discrete_sequence=[color], histnorm='percent')
    fig_first_org.update_yaxes(title=translate('Percentage'))
    fig_first_org.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig_first_org)

    st.write("#### " + translate('Distribution of Longest Duration in an Organization'))
    fig_longest_org = px.histogram(data, y='أطول مدة جهة يعمل بها', color_discrete_sequence=[color], histnorm='percent')
    fig_longest_org.update_yaxes(title=translate('Percentage'))
    fig_longest_org.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig_longest_org)

elif selected == "Contact" or selected == "اتصل بنا":
    st.write("### " + translate('Contact Information'))
    st.markdown("""
    <style>
        .contact-info {
            font-size: 18px;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            align-items: start;
        }
        .contact-info p {
            display: flex;
            align-items: center;
        }
        .contact-info p img {
            margin-right: 10px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
        .contact-info a {
            color: #FF6347;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="contact-info">
        <p>
            <img src="https://img.icons8.com/?size=100&id=I_5_kSloSWJW&format=png&color=000000" width="20" height="20" alt="User Icon"/>
            <strong>{translate('Salman Alshehri')}</strong>
        </p>
        <p>
            <img src="https://img.icons8.com/fluency/48/000000/email-open.png" width="20" height="20" alt="Email Icon"/>
             <a href="mailto:salman.awad@shehri.net">salman.awad@shehri.net</a>
        </p>
        <p>
            <img src="https://img.icons8.com/fluency/48/000000/linkedin.png" width="20" height="20" alt="LinkedIn Icon"/>
             <a href="https://www.linkedin.com/in/salshehri60/" target="_blank">https://www.linkedin.com/in/salshehri60/</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
