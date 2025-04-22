import React from 'react';
import {IntroSection} from './IntroSection';
import {SituationForm} from './SituationForm';

interface AppContentProps {
    onSituationSubmit: (situation: string) => void;
}

export const AppContent: React.FC<AppContentProps> = ({onSituationSubmit}) => {
    return (
        <div className="tg-content">
            <IntroSection/>
            <SituationForm onSubmit={onSituationSubmit}/>
        </div>
    );
};
