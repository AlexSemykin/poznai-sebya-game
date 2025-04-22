import { useState, useEffect } from 'react'
import './App.css'

function App() {
    const [isLoading, setIsLoading] = useState(true)
    const [userSituation, setUserSituation] = useState('')

    useEffect(() => {
        // Инициализация Telegram Mini App API
        const telegram = window.Telegram?.WebApp

        if (telegram) {
            // Уведомление Telegram, что приложение готово
            telegram.ready()

            // Настройка основного цвета из темы Telegram
            document.documentElement.style.setProperty('--tg-theme-button-color', telegram.themeParams?.button_color || '#50a8eb')
            document.documentElement.style.setProperty('--tg-theme-bg-color', telegram.themeParams?.bg_color || '#ffffff')
            document.documentElement.style.setProperty('--tg-theme-text-color', telegram.themeParams?.text_color || '#000000')
        }

        setIsLoading(false)
    }, [])

    const handleSubmit = () => {
        const telegram = window.Telegram?.WebApp
        if (telegram) {
            telegram.sendData(JSON.stringify({ 
                action: 'situation_submitted',
                situation: userSituation 
            }))
        }
    }

    if (isLoading) {
        return <div className="loading">Загрузка...</div>
    }

    return (
        <div className="tg-app">
            <header className="tg-header">
                <h1 className="app-title">Пространство Целостности</h1>
            </header>

            <div className="tg-content">
                <div className="intro-banner">
                    <div className="star-icon">🌟</div>
                    <h2>Добро пожаловать в Пространство Целостности!</h2>
                    <div className="star-icon">🌟</div>
                </div>

                <div className="tg-card description-card">
                    <p>Ты находишься в диалоговом пространстве, где внутренние конфликты превращаются в точки осознания.</p>
                    
                    <p>Этот бот помогает распознать скрытую дуальность внутри тебя — противоположные качества, между которыми возникло напряжение.</p>
                    
                    <p>Шаг за шагом ты получишь мягкий, но точный план выхода из внутреннего конфликта — не подавляя, а принимая оба полюса как часть своей целостной природы.</p>
                </div>

                <div className="tg-card situation-card">
                    <h3>Опиши свою ситуацию</h3>
                    <p className="hint-text">И мы вместе увидим, где спрятан дар</p>
                    
                    <textarea 
                        className="situation-input"
                        placeholder="Опиши ситуацию, которая тебя беспокоит..."
                        value={userSituation}
                        onChange={(e) => setUserSituation(e.target.value)}
                        rows={4}
                    />
                    
                    <button 
                        className="tg-button"
                        onClick={handleSubmit}
                        disabled={!userSituation.trim()}
                    >
                        Отправить
                    </button>
                </div>
            </div>
        </div>
    )
}

// Добавление типов для Telegram WebApp
declare global {
    interface Window {
        Telegram?: {
            WebApp: {
                ready: () => void;
                sendData: (data: string) => void;
                themeParams?: {
                    button_color?: string;
                    bg_color?: string;
                    text_color?: string;
                };
                initDataUnsafe?: {
                    user?: {
                        first_name?: string;
                    };
                };
            };
        };
    }
}

export default App
