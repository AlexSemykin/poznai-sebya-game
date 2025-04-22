import { useEffect, useState } from 'react';
import '../types/telegram.types';
import { TelegramAppData } from '../types/telegram.types';

interface UseTelegramAppReturn {
  isLoading: boolean;
  sendData: (data: TelegramAppData) => void;
}

export const useTelegramApp = (): UseTelegramAppReturn => {
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const telegram = window.Telegram?.WebApp;

    if (telegram) {
      // Уведомление Telegram, что приложение готово
      telegram.ready();

      // Настройка основного цвета из темы Telegram
      document.documentElement.style.setProperty('--tg-theme-button-color', telegram.themeParams?.button_color || '#50a8eb');
      document.documentElement.style.setProperty('--tg-theme-bg-color', telegram.themeParams?.bg_color || '#ffffff');
      document.documentElement.style.setProperty('--tg-theme-text-color', telegram.themeParams?.text_color || '#000000');
    }

    setIsLoading(false);
  }, []);

  const sendData = (data: TelegramAppData): void => {
    const telegram = window.Telegram?.WebApp;
    if (telegram) {
      telegram.sendData(JSON.stringify(data));
    }
  };

  return {
    isLoading,
    sendData
  };
};
