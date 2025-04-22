export interface TelegramWebApp {
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
}

// Базовый интерфейс для всех данных, отправляемых через WebApp
export interface TelegramAppDataBase {
    action: string;
}

// Интерфейс для данных с ситуацией
export interface SituationSubmittedData extends TelegramAppDataBase {
    action: 'situation_submitted';
    situation: string;
}

// Объединенный тип для всех возможных данных WebApp
export type TelegramAppData = SituationSubmittedData | (TelegramAppDataBase & Record<string, unknown>);

declare global {
    interface Window {
        Telegram?: {
            WebApp: TelegramWebApp;
        };
    }
}
