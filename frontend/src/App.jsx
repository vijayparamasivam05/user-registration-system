import { useState } from 'react';
import './App.css';

const fields = [
  { name: 'username', label: 'ユーザー名', type: 'text' },
  { name: 'email', label: 'メールアドレス', type: 'email' },
  { name: 'password', label: 'パスワード', type: 'password' },
  { name: 'tel', label: '電話番号', type: 'text' },
];

const validateForm = (formData) => {
  const errors = {};

  if (formData.username.length < 3) {
    errors.username = 'ユーザー名は3文字以上必要です。';
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(formData.email)) {
    errors.email = '正しいメールアドレスを入力してください。';
  }

  const pw = formData.password;
  if (pw.length < 8 || !/[A-Z]/.test(pw) || !/[a-z]/.test(pw) || !/\d/.test(pw)) {
    errors.password = 'パスワードは8文字以上、大文字・小文字・数字を含めてください。';
  }

  if (formData.tel && !/^\d+$/.test(formData.tel)) {
    errors.tel = '電話番号は数字のみで入力してください。';
  }

  if (!formData.pref) {
    errors.pref = '都道府県を選択してください。';
  }

  return errors;
};

function App() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    tel: '',
    pref: '',
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validateForm(formData);
    setErrors(validationErrors);
    setSubmitted(true);

    if (Object.keys(validationErrors).length === 0) {
      alert('バリデーション成功！（次はAPI連携）');
    }
  };

  return (
    <div className="container">
      <h2>ユーザー登録</h2>

      {submitted && Object.keys(errors).length > 0 && (
        <div className="error-summary">
          <ul>
            {Object.values(errors).map((err, index) => (
              <li key={index}>{err}</li>
            ))}
          </ul>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {fields.map(({ name, label, type }) => (
          <div className="form-group" key={name}>
            <label htmlFor={name}>{label}</label>
            <input
              type={type}
              id={name}
              name={name}
              value={formData[name]}
              onChange={handleChange}
            />
          </div>
        ))}

        <div className="form-group">
          <label htmlFor="pref">都道府県</label>
          <select name="pref" value={formData.pref} onChange={handleChange}>
            <option value="">選択してください</option>
            <option value="1">東京</option>
            <option value="2">大阪</option>
          </select>
        </div>

        <button type="submit">登録</button>
      </form>
    </div>
  );
}

export default App;
