import { createTheme, ThemeProvider } from '@mui/material/styles';
import React from 'react';

import { Route, BrowserRouter, Routes } from 'react-router-dom';
import HomePage from './pages/home';
import BasicTabs from './pages/SignUpTabs';
import SignInTab from './pages/SignInTabs';
import UserProfile from './component/UserProfile';
import BottomBar from './component/BottomBar';
import FollowPage from './pages/FollowPage';
import UploadCard from './component/UploadCard';
import PrimarySearchAppBar from './pages/NewHome';
// eslint-disable-next-line react/prop-types
function ChildComponent({ userName }) {
  return (
    <UserProfile
      userName={userName}
    />
  );
}

function App() {
  const theme = createTheme();
  const userName2 = localStorage.getItem('username');
  return (
    <BrowserRouter>
      <ThemeProvider theme={theme} />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="signup" element={<BasicTabs />} />
        <Route path="signin" element={<SignInTab />} />
        <Route path="userprofile" element={<ChildComponent userName={userName2} />} />
        <Route path="following" element={<FollowPage />} />
        <Route path="videoupload" element={<UploadCard />} />
        <Route path="newhome" element={<PrimarySearchAppBar />} />
      </Routes>
      <BottomBar />
    </BrowserRouter>

  );
}

export default App;
