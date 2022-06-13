import React, { useRef } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import FingerprintOutlinedIcon from '@material-ui/icons/FingerprintOutlined';
import Link from '@material-ui/core/Link';

function MadeWithLove() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      <Link color="inherit" href="https://github.com/tianyachen/StreamSocket">
        Built by StreamSocket Team
      </Link>
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignUp() {
  const classes = useStyles();

  const email = useRef(null);
  const username = useRef(null);
  const password = useRef(null);

  const handleLogIn = async () => {
    console.log(email.current?.value); // expect the password value but undefined get
    console.log(username.current?.value); // expect the password value but undefined get
    console.log(password.current?.value); // expect the password value but undefined get

    fetch(`http:/206.12.64.197:8000/all?email=${email}&username=${username}&password=${password}`, {
      method: 'GET',
    }).then((res) => {
      res.json();
    }).then((result) => {
      console.log(result);
    });
  };
  // function getSmsCode() {
  //   fetch('http://127.0.0.1:8000/users', {
  //     method: 'GET',
  //   }).then((res) => res.json()).then(
  //     (result) => {
  //       console.log(result);
  //     },
  //   );
  // }
  return (
    <Container
      component="main"
      maxWidth="xs"
    >

      <CssBaseline />
      <div
        className={classes.paper}
      >
        <Avatar className={classes.avatar}>
          <FingerprintOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleLogIn}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="Email Address or Phone Number"
                name="email"
                autoComplete="email"
                inputRef={email}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="UserName"
                label="User Name"
                name="userName"
                autoComplete="uname"
                inputRef={username}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                inputRef={password}
              />
            </Grid>

            <Grid item xs={12}>

              <FormControlLabel
                control={<Checkbox value="allowExtraEmails" color="primary" />}
                label="I am older than 13 years old."
              />

            </Grid>

          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign Up
          </Button>
        </form>
      </div>
      <Box mt={5}>
        <MadeWithLove />
      </Box>
    </Container>
  );
}