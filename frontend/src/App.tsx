import './App.css';
import { useTelegramApp } from './hooks/useTelegramApp';
import { Header } from './components/Header';
import { AppContent } from './components/AppContent';
import { LoadingScreen } from './components/LoadingScreen';

function App() {
    const { isLoading, sendData } = useTelegramApp();

    const handleSituationSubmit = (situation: string) => {
        sendData({ 
            action: 'situation_submitted',
            situation 
        });
    };

    if (isLoading) {
        return <LoadingScreen />;
    }

    return (
        <div className="tg-app">
            <Header />
            <AppContent onSituationSubmit={handleSituationSubmit} />
        </div>
    );
}

export default App;
