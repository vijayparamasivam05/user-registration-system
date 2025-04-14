import { useState, useEffect } from 'react';
import { registerUser } from './api';
import './App.css';

const App = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [tel, setTel] = useState('');
  const [pref, setPref] = useState('');
  const [formErrors, setFormErrors] = useState([]);
  const [apiErrors, setApiErrors] = useState([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [prefList, setPrefList] = useState([]);

  useEffect(() => {
    const fetchPrefectures = async () => {
      const response = await fetch('http://localhost:8000/accounts/prefs/');
      const data = await response.json();
      setPrefList(data);
    };
    fetchPrefectures();
  }, []);

  const validateForm = () => {
    const errors = [];

    if (!username) {
      errors.push("ユーザー名は必須です。");
    } else if (username.length < 3) {
      errors.push("ユーザー名は3文字以上で入力してください。");
    }

    if (!email) {
      errors.push("メールアドレスは必須です。");
    }

    if (!password) {
      errors.push("パスワードは必須です。");
    } else {
      if (password.length < 8) {
        errors.push("パスワードは8文字以上である必要があります。");
      }
      if (!/[A-Z]/.test(password)) {
        errors.push("パスワードには1つ以上の大文字を含めてください。");
      }
      if (!/[a-z]/.test(password)) {
        errors.push("パスワードには1つ以上の小文字を含めてください。");
      }
      if (!/\d/.test(password)) {
        errors.push("パスワードには1つ以上の数字を含めてください。");
      }
    }

    if (password !== passwordConfirmation) {
      errors.push("パスワードが一致しません。");
    }

    if (!tel) {
      errors.push("電話番号は必須です。");
    } else {
      if (!/^\d+$/.test(tel)) {
        errors.push("電話番号は数字のみで入力してください。");
      }
      if (tel.length < 10 || tel.length > 20) {
        errors.push("電話番号は10文字以上20文字以下である必要があります。");
      }
    }

    if (!pref) {
      errors.push("都道府県を選択してください。");
    }

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormErrors([]);
    setApiErrors([]);
    setSuccessMessage('');

    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setFormErrors(validationErrors);
      return;
    }

    const userData = {
      username,
      email,
      password,
      password_confirmation: passwordConfirmation,
      tel,
      pref,
    };

    try {
      await registerUser(userData);
      setSuccessMessage('ユーザーの登録が完了しました！');
      setUsername('');
      setEmail('');
      setPassword('');
      setPasswordConfirmation('');
      setTel('');
      setPref('');
    } catch (errorMessages) {
      setApiErrors(errorMessages);
    }
  };

  return (
    <div className="container">
      <h2>User Registration</h2>

      {successMessage && (
        <div className="success">{successMessage}</div>
      )}

      {(formErrors.length > 0 || apiErrors.length > 0) && (
        <div className="error-summary">
          <ul>
            {formErrors.map((err, idx) => (
              <li key={`form-${idx}`}>{err}</li>
            ))}
            {apiErrors.map((err, idx) => (
              <li key={`api-${idx}`}>{err}</li>
            ))}
          </ul>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Phone Number</label>
          <input
            type="text"
            value={tel}
            onChange={(e) => setTel(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Prefecture</label>
          <select
            value={pref}
            onChange={(e) => setPref(e.target.value)}
            required
          >
            <option value="">選択してください</option>
            {prefList.map((prefItem) => (
              <option key={prefItem.id} value={prefItem.id}>
                {prefItem.name}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default App;
