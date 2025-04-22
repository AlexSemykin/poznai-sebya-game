import { useState } from 'react';

interface SituationFormProps {
  onSubmit: (situation: string) => void;
}

export const SituationForm: React.FC<SituationFormProps> = ({ onSubmit }) => {
  const [userSituation, setUserSituation] = useState('');
  
  const handleSubmit = () => {
    onSubmit(userSituation);
  };
  
  return (
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
  );
};
