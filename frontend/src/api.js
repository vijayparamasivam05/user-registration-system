const API_URL = 'http://localhost:8000/accounts/register/';

export const registerUser = async (userData) => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (!response.ok) {
      // 400エラーのとき、複数のメッセージを配列にする
      if (response.status === 400 && typeof data === 'object') {
        const messages = [];
        for (const key in data) {
          if (Array.isArray(data[key])) {
            data[key].forEach((msg) => messages.push(msg));
          } else if (typeof data[key] === 'string') {
            messages.push(data[key]);
          }
        }
        throw messages;
      }

      // その他のエラー
      throw [data.detail || 'エラーが発生しました。'];
    }

    return data;
  } catch (error) {
    console.error('Error registering user:', error);
    // 常に配列としてフロントに投げる
    throw Array.isArray(error) ? error : [error.message || 'エラーが発生しました。'];
  }
};
