import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def pluralMarriageFig(man, dob, lastName):
    df = pd.read_csv('data/Plural Marriage/Plural Marriage - {}.csv'.format(man))
    birth_dates = pd.to_datetime(df['Birth'], format='mixed')
    marriage_dates = pd.to_datetime(df['Marriage Date'], format='mixed')
    ages_wives = marriage_dates - birth_dates
    ages_man = marriage_dates - pd.to_datetime(dob)

    ages_wives = ages_wives / np.timedelta64(1, 'Y')
    ages_man = ages_man / np.timedelta64(1, 'Y')

    text = df['Wife'] + '<br>' + 'Marriage: ' + df['Marriage Date'] + '<br>'
    text += 'Age: ' + np.floor(ages_wives).astype(int).astype(str) + '<br>'
    text += 'Age of {}: '.format(lastName) + np.floor(ages_man).astype(int).astype(str) + '<br>'
    text += 'Children: ' + df['Children'].astype(str) + '<br>'
    
    hovertemplate = '%{hovertext}<extra></extra>'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ages_man, y=ages_wives, mode='markers', name='Ages', hovertext=text, hovertemplate=hovertemplate))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        height=700,
        title='Wives of {}'.format(man), 
        xaxis_title='Age of {} on Marriage Date'.format(lastName), 
        yaxis_title='Age of Wives on Marriage Date', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    
    return fig


def app():
    st.title('Plural Marriage')

    col1, col2 = st.columns([1, 4])
    men = ['Joseph Smith', 'Brigham Young', 'Heber C Kimball', 'John Taylor', 'Wilford Woodruff', 'Lorenzo Snow', 'Joseph F Smith', 'John D Lee', 'Willard Richards']
    with col1:
        personSelected = st.radio('Plural Marriage Practitioner', men)
    
    if personSelected == 'Joseph Smith':
        df = pd.read_csv('data/Plural Marriage/Plural Marriage - Joseph Smith.csv')
        birth_dates = pd.to_datetime(df['Birth Approx'])
        marriage_dates = pd.to_datetime(df['Marriage Date Approx'])
        ages_wives = marriage_dates - birth_dates
        ages_joseph = marriage_dates - pd.to_datetime('December 23, 1805')

        ages_wives = ages_wives / np.timedelta64(1, 'Y')
        ages_joseph = ages_joseph / np.timedelta64(1, 'Y')

        text = df['Wife'] + '<br>' + 'Marriage: ' + df['Marriage Date'] + '<br>' 
        text += 'Age: ' + df['Age'] + '<br>'
        text += 'Age of Smith: ' + np.floor(ages_joseph).astype(int).astype(str) + '<br>'
        text += 'Marital Status: ' + df['Marital status at time of sealing'] + '<br>'
        hovertemplate = '%{hovertext}<extra></extra>'

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages_joseph, y=ages_wives, mode='markers', name='Ages', hovertext=text, hovertemplate=hovertemplate))
        fig.update_layout(
            margin=dict(l=10, r=10, t=100, b=20),
            height=700,
            title='Wives of Joseph Smith', 
            xaxis_title='Age of Smith on Marriage Date', 
            yaxis_title='Age of Wives on Marriage Date', 
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        )
    elif personSelected == 'Brigham Young':
        df = pd.read_csv('data/Plural Marriage/Plural Marriage - Brigham Young.csv')
        birth_dates = pd.to_datetime(df['Birth'])
        marriage_dates = pd.to_datetime(df['Marriage Date Approx'], format='mixed')
        ages_wives = marriage_dates - birth_dates
        ages_brigham = marriage_dates - pd.to_datetime('June 1, 1801')

        ages_wives = ages_wives / np.timedelta64(1, 'Y')
        ages_brigham = ages_brigham / np.timedelta64(1, 'Y')

        text = df['Wife'] + '<br>' + 'Marriage: ' + df['Marriage Date'] + '<br>'
        text += 'Age: ' + df["Wife's Age at Marriage"].astype(str) + '<br>'
        text += 'Age of Young: ' + np.floor(ages_brigham).astype(int).astype(str) + '<br>'
        text += 'Marital Status: ' + df['Marital Status at Time of Marriage'] + '<br>'
        text += 'Type of Union: ' + df['Type of Union'] + '<br>'
        text += 'Children: ' + df['Children'] + '<br>'
        
        hovertemplate = '%{hovertext}<extra></extra>'

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages_brigham, y=ages_wives, mode='markers', name='Ages', hovertext=text, hovertemplate=hovertemplate))
        fig.update_layout(
            margin=dict(l=10, r=10, t=100, b=20),
            height=700,
            title='Wives of Brigham Young', 
            xaxis_title='Age of Young on Marriage Date', 
            yaxis_title='Age of Wives on Marriage Date', 
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        )

    elif personSelected == 'Heber C Kimball':
        fig = pluralMarriageFig(personSelected, 'June 14, 1801', 'Kimball')
    
    elif personSelected == 'John Taylor':
        fig = pluralMarriageFig(personSelected, '1 November 1808', 'Taylor')            
        
    elif personSelected == 'Wilford Woodruff':
        fig = pluralMarriageFig(personSelected, '1 March 1807', 'Woodruff')

    elif personSelected == 'Lorenzo Snow':
        fig = pluralMarriageFig(personSelected, 'April 3, 1814', 'Snow')

    elif personSelected == 'Joseph F Smith':
        fig = pluralMarriageFig(personSelected, 'November 13, 1838', 'Smith')

    elif personSelected == 'John D Lee':
        fig = pluralMarriageFig(personSelected, 'September 6, 1812', 'Lee')

    elif personSelected == 'Willard Richards':
        fig = pluralMarriageFig(personSelected, 'June 24, 1804', 'Richards')

    with col2:
        st.plotly_chart(fig, use_container_width=True)
        if personSelected == 'Joseph Smith':
            st.write('See Wikipedia: [List of Josepth Smith\'s Wives](https://en.wikipedia.org/wiki/List_of_Joseph_Smith\'s_wives)')
            st.write('See [Biographies of Joseph\'s Plural Wives by Brian Hales](https://josephsmithspolygamy.org/plural-wives-overview/)')
            st.write('See [In Sacred Loneliness By Todd Compton](https://www.overdrive.com/media/5618863/in-sacred-loneliness)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWJY-BPD)')
        elif personSelected == 'Brigham Young':
            st.write('See Wikipedia: [List of Brigham Young\'s Wives](https://en.wikipedia.org/wiki/List_of_Brigham_Young\'s_wives)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWJH-9QN)')
        elif personSelected == 'Heber C Kimball':
            st.write('See Wikipedia: [Heber C. Kimball](https://en.wikipedia.org/wiki/Heber_C._Kimball#Wives_and_children)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWNP-GNM)')
        elif personSelected == 'John Taylor':
            st.write('See Wikipedia: [John Taylor](https://en.wikipedia.org/wiki/John_Taylor_(Mormon)#Family)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWJC-VF5)')
            st.write('*Note: Eight of the sealings may not have been considered full marriages, and they did not live together.')
        elif personSelected == 'Wilford Woodruff':
            st.write('See Wikipedia: [Wilford Woodruff](https://en.wikipedia.org/wiki/Wilford_Woodruff#Marriage_and_family)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWNT-8NB)')
        elif personSelected == 'Lorenzo Snow':
            st.write('See Wikipedia: [Lorenzo Snow](https://en.wikipedia.org/wiki/Lorenzo_Snow#Wives_and_children)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KW84-5CT)')
        elif personSelected == 'Joseph F Smith':
            st.write('See Wikipedia: [Joseph F. Smith](https://en.wikipedia.org/wiki/Joseph_F._Smith#Marriages_and_family)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWCW-8ZJ)')
        elif personSelected == 'Willard Richards':
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWJ5-X12)')
            with st.expander('Note on marriages to Sarah and Nanny Longstroth'):
                st.write('''
                When Joseph Smith told Grandpa [i.e., Willard Richards] to take another wife, he had no one in mind; 
                so the Prophet said, "Willard, what about some of the women you knew in England?" And immediately
                Grandfather thought of the Longstroth family and how they had taken good care of him when he was so 
                ill. The Longstroths had come to America and were living in St. Louis, and Willard went down there 
                and asked the parents for Sarah and Nanny. Sarah was sixteen, and Nanny was fourteen. The parents 
                thought Nanny was too young, so Willard said, "Let me marry her, and she can come back home and stay 
                with you and when you feel that she is ready you can send her to me." With the consent of the girls 
                this was agreed upon. A few weeks later, Grandpa Longstroth brought the girls to Nauvoo. They married 
                Dr. Willard Richards in January 1843. Joseph Smith performed the ceremony. Nanny returned to St. Louis 
                with her father, and Sarah may have stayed in Nauvoo for awhile, but later was with her family in 
                Rockport, Mo. where they were living in 1843 and early 1844. The Longstroths moved to Nauvoo in Mar 1844 
                and it is known that Sarah was living with her family when Willarďs wife Jennetta died (July 1845). 
                Sarah and Nanny were sealed to Willard Richards in the Nauvoo Temple Jan[uary] 22 and 25, 1846 and it was 
                after this time that the marriages were consumated.\n
                -- Ann Richards Martin, "Sarah Longstroth (1826-1858)," in Richards Family History, edited by Joseph Grant Stevenson, 
                (Provo, Utah: Stevenson's Genealogical Center, 1991), 3:279; see also p. 285.
                ''')
        elif personSelected == 'John D Lee':
            st.write('See Wikipedia: [John D. Lee](https://en.wikipedia.org/wiki/John_D._Lee)')
            st.write('See [Family Search Record](https://www.familysearch.org/tree/person/details/KWN4-6TW)')
            with st.expander('Notes'):
                st.write('''
                Lee was convicted as a mass murderer for his complicity in the [Mountain Meadows Massacre](https://en.wikipedia.org/wiki/Mountain_Meadows_Massacre), sentenced to death and was executed in 1877.\n
                **Marriage to Mary Ann Williams:**
                When she was still very young, Mary Ann Williams was sealed to John Doyle Lee as a plural wife; however the marriage 
                was never consummated and she fell in love with John D. Lee's son, John Alma Lee (who was much nearer her own age). 
                As soon as she made her feelings known to John D. Lee, he dissolved their marriage and sealed Mary Ann to his son Alma.
                -- [Some descendants of John Doyle Lee, Chapter 17](http://www.wadhome.org/lee/chapter_17.html)\n
                **First child of wives with their date of birth:**\n
                Sarah Caroline Williams - Harvey Parley Lee - 1 October 1852\n
                Nancy Bean - Cornelia Lee - 15 January 1846\n
                Mary Leah Groves - Erastus Franklin Lee - 1 March 1854\n
                Ann Gordge - Samuel James Lee - 14 March 1867
                ''')
            
    df = pd.read_csv('data/Plural Marriage/Number of wives.csv')
    df = df.sort_values('Number of Wives', ascending=False)

    text = df['Practitioner'] + '<br>' + 'Number of Wives: ' + df['Number of Wives'].astype(str) + '<br>' + 'Position: ' + df['Position']
    hovertemplate = '%{hovertext}<extra></extra>'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Number of Wives'], y=df['Practitioner'], orientation='h', hovertext=text, hovertemplate=hovertemplate))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=800,
        title='Number of Wives of Plural Marriage Practitioners',
        xaxis_title='Number of Wives',
        yaxis={'autorange': 'reversed'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('There may be some inaccuracies in the number of wives. See Wikipedia: [List of Latter Day Saint practitioners of plural marriage](https://en.wikipedia.org/wiki/List_of_Latter_Day_Saint_practitioners_of_plural_marriage)')
