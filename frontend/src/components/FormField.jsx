function FormField({ label, name, type = "text", value, error, onChange, options }) {
    return (
      <div className="field">
        <label>{label}</label>
        {options ? (
          <select name={name} value={value} onChange={onChange}>
            <option value="">選択してください</option>
            {options.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        ) : (
          <input type={type} name={name} value={value} onChange={onChange} />
        )}
        {error && <div className="error">{error}</div>}
      </div>
    );
  }
  
  export default FormField;
  