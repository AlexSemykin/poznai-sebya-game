import { useState, useEffect } from 'react'
import './App.css'

function App() {
    const [userName, setUserName] = useState('Пользователь')
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        // Инициализация Telegram Mini App API
        const telegram = window.Telegram?.WebApp

        if (telegram) {
            // Уведомление Telegram, что приложение готово
            telegram.ready()

            // Получение имени пользователя из Telegram
            if (telegram.initDataUnsafe?.user?.first_name) {
                setUserName(telegram.initDataUnsafe.user.first_name)
            }

            // Настройка основного цвета из темы Telegram
            document.documentElement.style.setProperty('--tg-theme-button-color', telegram.themeParams?.button_color || '#50a8eb')
            document.documentElement.style.setProperty('--tg-theme-bg-color', telegram.themeParams?.bg_color || '#ffffff')
            document.documentElement.style.setProperty('--tg-theme-text-color', telegram.themeParams?.text_color || '#000000')
        }

        setIsLoading(false)
    }, [])

    const handleMainAction = () => {
        const telegram = window.Telegram?.WebApp
        if (telegram) {
            telegram.sendData(JSON.stringify({ action: 'main_button_clicked' }))
        }
    }

    if (isLoading) {
        return <div className="loading">Загрузка...</div>
    }

    return (
        <div className="tg-app">
            <header className="tg-header">
                <h1>Telegram Mini App</h1>
                <p className="welcome-text">Привет, {userName}!</p>
            </header>

            <div className="tg-content">
                <div className="tg-card">
                    <h2>О приложении</h2>
                    <p>Это мини-приложение для Telegram, разработанное с использованием React и Vite.</p>
                </div>

                <div className="tg-card">
                    <h2>Функции</h2>
                    <ul className="feature-list">
                        <li>Интеграция с Telegram</li>
                        <li>Адаптивный дизайн</li>
                        <li>Поддержка тем Telegram</li>
                    </ul>
                </div>

                <button className="tg-button" onClick={handleMainAction}>
                    Выполнить действие
                </button>
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