import React, { useEffect, useState } from 'react';
import {
  Widget,
  addResponseMessage,
  addUserMessage,
  toggleWidget,
} from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';

import logo from './logo.svg';

const STEPS = {
  NAME: 'Hey! What is your name?',
  SYMPTOM: 'Please enter the symptom you are experiencing',
  DURATION: 'Since how many days have you been experiencing them?',
  QUERIES: 'queries',
};

var steps = [STEPS.NAME, STEPS.SYMPTOM, STEPS.DURATION, STEPS.QUERIES];

function App() {
  const getCustomLauncher = (handleToggle) => (
    <button
      onClick={() => {
        console.log('clicked');
        toggleWidget();
        // handleToggle();
      }}>
      This is my launcher component!
    </button>
  );

  const [stepId, setStepId] = useState(0);
  const [name, setName] = useState('');
  const [symptom, setSymptom] = useState('');
  const [duration, setDuration] = useState('');
  const [toggle, setToggle] = useState(false);
  const [query, setQuery] = useState([]);
  const [queryId, setQueryId] = useState(-1);
  const [queryRes, setQueryRes] = useState([]);
  useEffect(() => {}, []);

  const handleNewUserMessage = (newMessage) => {
    console.log(`New message incoming! ${newMessage}`);
    console.log('queryId ' + queryId);
    console.log('queryRes ' + queryRes);
    console.log('stepId ' + stepId);
    console.log('query.length ' + query.length);
    if (stepId == 0) {
      addResponseMessage(steps[stepId]);
      setStepId(stepId + 1);

      return;
    }
    if (stepId == 1) {
      addResponseMessage(steps[stepId]);
      setStepId(stepId + 1);
      setName(newMessage);
      return;
    }

    if (stepId == 2) {
      addResponseMessage(steps[stepId]);
      setStepId(stepId + 1);
      setSymptom(newMessage);
      return;
    }

    if (stepId == 3 && queryId == -1) {
      setDuration(newMessage);

      //api call we get query array
      const resQuery = ['a', 'b', 'c'];
      setQueryId(0);
      setQuery(resQuery);
      addResponseMessage(resQuery[0]);
      setQueryId(1);
      return;
    }

    if (stepId == 3 && queryId < query.length) {
      if (newMessage == 'yes') setQueryRes([...queryRes, query[queryId]]);
      addResponseMessage(query[queryId]);
      setQueryId(queryId + 1);
      return;
    }

    if (stepId == 3 && queryId == query.length) {
      console.log('result');
      addResponseMessage('hdfg');

      // api call to get result
      return;
    }

    // Now send the message throught the backend API
  };
  return (
    <div className="App">
      <button
        onClick={() => {
          setToggle(!toggle);
        }}>
        <Widget
          handleNewUserMessage={handleNewUserMessage}
          profileAvatar={logo}
          fullScreenMode={toggle}
          title="My new awesome title"
          subtitle="And my cool subtitle"
        />
      </button>
    </div>
  );
}

export default App;
