import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & PREMIUM CYBER THEME ---
st.set_page_config(
    page_title="ShieldOSINT Nexus Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Внедрение кастомного CSS для создания футуристичного Dark-интерфейса
st.markdown("""
    <style>
    /* Главный фон и шрифты */
    .main { background-color: #0b0f19; color: #e2e8f0; }
    h1, h2, h3 { color: #38bdf8 !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    
    /* Стилизация контейнеров и карточек */
    div.stBlock { background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; }
    
    /* Премиальные кибер-метрики с неоновым свечением */
    .cyber-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .metric-critical { border-left: 5px solid #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.15); }
    .metric-warning { border-left: 5px solid #f59e0b; box-shadow: 0 0 15px rgba(245, 158, 11, 0.15); }
    .metric-success { border-left: 5px solid #10b981; box-shadow: 0 0 15px rgba(16, 185, 129, 0.15); }
    .metric-info { border-left: 5px solid #3b82f6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.15); }
    
    /* Стили для кастомных бэджей (Badges) */
    .badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-crit { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid #ef4444; }
    .badge-warn { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid #f59e0b; }
    .badge-succ { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid #10b981; }
    
    /* Блоки с кодом и логами */
    code { color: #f472b6 !important; background-color: #1e1e2e !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ИНИЦИАЛИЗАЦИЯ ДАННЫХ (БАЗА ИНЦИДЕНТОВ) ---
if "incidents" not in st.session_state or len(st.session_state.incidents) == 0:
    st.session_state.incidents = [
        {"id": "NEX-9041", "platform": "Meta Ads (Реклама)", "source": "Meta Реклама -> Кабинет 'Каспи_Бонус_2026'", "text": "Внимание! Президент Касым-Жомарт Токаев утвердил новые выплаты для семей. Каждый гражданин РК может получить компенсацию от 215 000 тенге из государственного фонда поддержки. Проверьте ваш ИИН на официальном портале.", "category": "Фейковые выплаты гос. органов", "risk_score": 98, "city": "Астана", "lat": 51.1605, "lon": 71.4704, "status": "Новый", "domain": "mne-gov-bonus.info", "date": datetime.now() - timedelta(minutes=45)},
        {"id": "NEX-9042", "platform": "TikTok", "source": "TikTok @lomtadze_invest_official", "text": "🔥 Срочно! Уникальная платформа «Каспи Автоматические Инвестиции». Вложи 30 000 KZT и система сама будет зарабатывать для вас по 95 000 KZT ежедневно. Михаил Ломтадзе лично гарантирует доход. Мест осталось всего 3, пиши мне в Telegram по ссылке в био!", "category": "Финансовая пирамида", "risk_score": 94, "city": "Алматы", "lat": 43.2389, "lon": 76.8897, "status": "В обработке", "domain": "kaspi-ai-cabinet.xyz", "date": datetime.now() - timedelta(hours=3)},
        {"id": "NEX-9043", "platform": "Telegram", "source": "Telegram @tenge_pump_arbitrazh", "text": "Раскрутка баланса на Kaspi/Halyk! Схема 100% рабочая, отзывы клиентов смотрите на канале. Вы скидываете 15 000 тенге — я прокручиваю их на бирже и возвращаю 120 000 тенге через 4 часа. Мой интерес — 20% после вашего получения.", "category": "Раскрутка счетов / Скаринг", "risk_score": 88, "city": "Шымкент", "lat": 42.3249, "lon": 69.5881, "status": "Новый", "domain": "N/A", "date": datetime.now() - timedelta(hours=5)},
        {"id": "NEX-9044", "platform": "Instagram (Посты)", "source": "Instagram @halyk_bank_prizes", "text": "🎁 Праздничный опрос в честь юбилея Halyk Bank! Ответьте на 3 простых вопроса и выиграйте гарантированный приз до 500 000 тенге на карту. Для получения выигрыша необходимо оплатить закрепительный платеж (комиссию банка) в размере 2400 тенге.", "category": "Фишинговый опрос с комиссией", "risk_score": 82, "city": "Караганда", "lat": 49.8018, "lon": 73.0911, "status": "Блокирован", "domain": "halyk-anniversary-win.cc", "date": datetime.now() - timedelta(days=1)}
    ]

# --- 3. СУПЕР ИИ-ДВИЖОК ОЦЕНКИ И КЛАССИФИКАЦИИ ---
def cyber_ai_analysis(text, platform_type):
    text_lower = text.lower()
    base_score = 45
    category = "Неопределенная угроза"
    
    # Эвристические маркеры скама
    if any(x in text_lower for x in ["выплат", "компенсац", "указ", "постановлен", "минеконом"]):
        category = "Фейковые выплаты гос. органов"
        base_score += 35
    elif any(x in text_lower for x in ["инвест", "ломтадзе", "пассивный доход", "вложи"]):
        category = "Финансовая пирамида"
        base_score += 25
    elif any(x in text_lower for x in ["раскрут", "прокрутка", "баланс", "скидываете"]):
        category = "Раскрутка счетов / Скаринг"
        base_score += 30
    elif any(x in text_lower for x in ["опрос", "выиграй", "приз", "комисси", "платеж"]):
        category = "Фишинговый опрос с комиссией"
        base_score += 20

    # Психологические триггеры манипуляции (Социальная инженерия)
    manipulation_triggers = ["срочно", "осталось всего", "мест", "прямо сейчас", "гарантир", "без риска", "успей"]
    for trigger in manipulation_triggers:
        if trigger in text_lower:
            base_score += 5
            
    if "meta ads" in platform_type.lower():
        base_score += 5

    # Поиск доменов
    import re
    urls = re.findall(r'(https?://[^\s]+)', text)
    domain = urls[0].split('//')[-1].split('/')[0] if urls else "N/A"
    if domain != "N/A": base_score += 5

    return min(base_score, 100), category, domain

# --- 4. СТРУКТУРА НАВИГАЦИИ (ВЕРХНИЙ БАР И СЛЕВА) ---
st.sidebar.markdown("<h2 style='text-align: center;'>🛡️ NEXUS CORE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px; color: #6b7280;'>Агентство по финансовому мониторингу РК</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

tab_choice = st.sidebar.radio(
    "ГЛАВНЫЕ МОДУЛИ СИСТЕМЫ",
    ["📊 Аналитический хаб SOC", "🛰️ Стриминг & Live-перехват", "⚡ Автоматический Takedown-центр"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Конфигурация парсинга")
src_platform = st.sidebar.selectbox("Медиа-источник", ["Meta Ads (Реклама)", "Telegram", "TikTok", "Instagram (Посты)"])
query_pattern = st.sidebar.text_input("Поисковый паттерн", "Каспи Инвест")
depth = st.sidebar.slider("Глубина анализа", 5, 50, 10)

# Эмуляция сбора данных при нажатии кнопки
if st.sidebar.button("📡 Начать перехват угроз", type="primary"):
    with st.sidebar.spinner("Инициализация OSINT-агентов..."):
        sim_text = f"⚡ СРОЧНО! Новый запуск платформы {query_pattern} для граждан Казахстана. Успей вложить 25000 тенге и получать пассивный доход. Ссылка активна прямо сейчас: https://secure-{query_pattern.lower().replace(' ', '')}-portal.ru"
        score, cat, dom = cyber_ai_analysis(sim_text, src_platform)
        
        cities_list = [
            {"n": "Алматы", "la": 43.2389, "lo": 76.8897}, 
            {"n": "Астана", "la": 51.1605, "lo": 71.4704},
            {"n": "Шымкент", "la": 42.3249, "lo": 69.5881}
        ]
        chosen_geo = np.random.choice(cities_list)
        
        new_inc = {
            "id": f"NEX-{np.random.randint(5000, 9999)}", "platform": src_platform,
            "source": f"{src_platform}: Поток по паттерну '{query_pattern}'", "text": sim_text,
            "category": cat, "risk_score": score, "city": chosen_geo["n"], 
            "lat": chosen_geo["la"], "lon": chosen_geo["lo"], "status": "Новый", 
            "domain": dom, "date": datetime.now()
        }
        st.session_state.incidents = [new_inc] + st.session_state.incidents
        st.sidebar.success("Перехват успешно завершен!")

df_main = pd.DataFrame(st.session_state.incidents)

# =====================================================================
# МОДУЛЬ 1: АНАЛИТИЧЕСКИЙ ХАБ SOC (Dashboard)
# =====================================================================
if tab_choice == "📊 Аналитический хаб SOC":
    st.title("📊 Аналитический хаб SOC ShieldOSINT")
    st.markdown("Глобальный мониторинг угроз информационной безопасности и мошеннических кампаний в РК.")
    st.markdown("---")
    
    # Стилизованные Кросс-метрики
    m_c1, m_c2, m_c3, m_c4 = st.columns(4)
    
    with m_c1:
        st.markdown(f"<div class='cyber-card metric-info'><p style='color: #6b7280; font-size:14px; margin:0;'>Всего инцидентов</p><h2 style='margin:0; color:#3b82f6;'>{len(df_main)}</h2></div>", unsafe_allow_html=True)
    with m_c2:
        crit_n = len(df_main[df_main['risk_score'] >= 90])
        st.markdown(f"<div class='cyber-card metric-critical'><p style='color: #6b7280; font-size:14px; margin:0;'>Критические риски (>90%)</p><h2 style='margin:0; color:#ef4444;'>{crit_n}</h2></div>", unsafe_allow_html=True)
    with m_c3:
        done_n = len(df_main[df_main['status'] == "Блокирован"])
        st.markdown(f"<div class='cyber-card metric-success'><p style='color: #6b7280; font-size:14px; margin:0;'>Нейтрализовано (Takedown)</p><h2 style='margin:0; color:#10b981;'>{done_n}</h2></div>", unsafe_allow_html=True)
    with m_c4:
        dom_n = len(df_main[df_main['domain'] != "N/A"])
        st.markdown(f"<div class='cyber-card metric-warning'><p style='color: #6b7280; font-size:14px; margin:0;'>Активные фишинг-домены</p><h2 style='margin:0; color:#f59e0b;'>{dom_n}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("###")
    
    # Графики Plotly High-End уровня
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("#### 📈 Структура угроз по ИИ-категориям")
        fig_pie = px.pie(
            df_main, names='category', hole=0.5,
            color_discrete_sequence=px.colors.sequential.Darkmint
        )
        fig_pie.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with g_col2:
        st.markdown("#### ⚡ Динамика распределения рисков по медиа-каналам")
        fig_bar = px.bar(
            df_main, x='platform', y='risk_score', color='category',
            barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Карта гео-активности скама
    st.markdown("#### 🗺️ Карта векторов атак социальной инженерии в регионах РК")
    df_main["dot_size"] = df_main["risk_score"] * 120
    st.map(df_main, latitude="lat", longitude="lon", size="dot_size")

# =====================================================================
# МОДУЛЬ 2: СТРИМИНГ & LIVE-ПЕРЕХВАТ (Live Feed)
# =====================================================================
elif tab_choice == "🛰️ Стриминг & Live-перехват":
    st.title("🛰️ Модуль Live-перехвата контента")
    st.markdown("Интерактивная панель мониторинга входящих подозрительных медиа-материалов.")
    st.markdown("---")
    
    # Инструменты фильтрации данных
    filt_c1, filt_c2 = st.columns([1, 2])
    with filt_c1:
        selected_platforms = st.multiselect("Фильтр источников", df_main['platform'].unique(), default=df_main['platform'].unique())
    with filt_c2:
        min_risk_slider = st.slider("Порог чувствительности Risk Score %", 50, 100, 70)
        
    df_filtered = df_main[(df_main['platform'].isin(selected_platforms)) & (df_main['risk_score'] >= min_risk_slider)]
    
    # Рендеринг карточек инцидентов
    for idx, row in df_filtered.iterrows():
        # Определение типа плашки
        if row['risk_score'] >= 90:
            badge_html = "<span class='badge badge-crit'>🔴 КРИТИЧЕСКИЙ РИСК</span>"
        elif row['risk_score'] >= 80:
            badge_html = "<span class='badge badge-warn'>🟡 СРЕДНЯЯ УГРОЗА</span>"
        else:
            badge_html = "<span class='badge badge-succ'>🟢 НИЗКИЙ РИСК</span>"
            
        with st.expander(f"Инцидент {row['id']} | [{row['platform']}] — {row['source'][:40]}..."):
            col_l, col_r = st.columns([3, 1])
            with col_l:
                st.markdown(f"<div>{badge_html} <b style='font-size:16px; margin-left:10px;'>{row['category']}</b></div>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top:10px; color:#9ca3af;'><b>Текст сообщения/промо-кампании:</b></p>", unsafe_allow_html=True)
                st.info(f"\"{row['text']}\"")
                
                if row['domain'] != "N/A":
                    st.markdown(f"🔗 **Инфраструктура (Фишинг-хост):** `{row['domain']}`")
                st.markdown(f"📍 **Региональный охват атаки:** {row['city']}")
            with col_r:
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                st.metric("Risk Score", f"{row['risk_score']}%")
                st.write(f"**Статус:** `{row['status']}`")
                st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# МОДУЛЬ 3: АВТОМАТИЧЕСКИЙ TAKEDOWN-ЦЕНТР (Takedown & Block)
# =====================================================================
elif tab_choice == "⚡ Автоматический Takedown-центр":
    st.title("⚡ Автоматизированный центр реагирования и блокировок")
    st.markdown("Быстрое формирование юридических кейсов и отправка предписаний на блокировку доменов и рекламных аккаунтов.")
    st.markdown("---")
    
    df_active = df_main[df_main['status'] != "Блокирован"]
    
    if len(df_active) == 0:
        st.success("🎉 Отлично! Все обнаруженные киберугрозы и мошеннические кампании заблокированы.")
    else:
        st.warning(f"🚨 В очереди на реагирование находится {len(df_active)} активных угроз.")
        
        for idx, row in df_active.iterrows():
            st.markdown(f"""
            <div style='background-color: #111827; border: 1px solid #374151; padding:15px; border-radius:8px; margin-bottom:15px;'>
                <span style='color:#ef4444; font-weight:bold;'>[{row['id']}]</span> — Платформа: <b>{row['platform']}</b> | Источник: <i>{row['source']}</i><br/>
                <small style='color:#6b7280;'>Категория угрозы: {row['category']} | Целевой хост: {row['domain']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            btn_c1, btn_c2 = st.columns(2)
            
            with btn_c1:
                if st.button(f"📋 Сформировать пакет доказательств", key=f"tk_doc_{row['id']}_{idx}"):
                    evidence_pack = f"""============================================================
ОФИЦИАЛЬНЫЙ ПАКЕТ ДОКАЗАТЕЛЬСТВ ДЛЯ БЛОКИРОВКИ ({row['id']})
============================================================
Генератор: ShieldOSINT Nexus AI Core
Целевое ведомство: АФМ РК / Министерство Культуры и Информации РК
Платформа нарушения: {row['platform']}
Доказательный текст: {row['text']}

ВЫЯВЛЕННЫЕ МАРКЕРЫ (IoC):
- Категория по ИИ-классификатору: {row['category']}
- Уровень угрозы национальной безопасности: {row['risk_score']}%
- Вредоносная сетевая ссылка: {row['domain']}

РЕКОМЕНДАЦИЯ:
Внести домен {row['domain']} в реестр блокировок МЦРИАП. Направить официальную жалобу в Meta/TikTok Trust & Safety для деактивации рекламного кабинета.
============================================================\n"""
                    st.code(evidence_pack, language="text")
            with btn_c2:
                if st.button(f"🚫 Заблокировать и отправить в АФМ", key=f"tk_block_{row['id']}_{idx}", type="primary"):
                    # Меняем статус в сессии
                    for incident in st.session_state.incidents:
                        if incident['id'] == row['id']:
                            incident['status'] = "Блокирован"
                    st.success(f"Запрос на блокировку кампании {row['id']} успешно отправлен в реестр АФМ через API Webhook!")
                    st.rerun()
