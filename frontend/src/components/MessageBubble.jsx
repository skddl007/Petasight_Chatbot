const RULE_LABELS = {
  city_temp: "Temperature",
  decimal: "Decimal",
  panic: "Mood",
};

export default function MessageBubble({
  role,
  content,
  backgroundColor,
  textColor,
  ruleApplied,
  meta,
}) {
  const isUser = role === "user";
  const style = isUser
    ? {}
    : {
        backgroundColor: backgroundColor || "#2a2a35",
        color: textColor || "#f4f4f5",
      };

  const hasBilingual = !isUser && meta?.original && meta?.translation;

  return (
    <div className={`message-row ${isUser ? "message-row--user" : "message-row--bot"}`}>
      {!isUser && ruleApplied && (
        <span className="message-rule" aria-label={`Color rule: ${RULE_LABELS[ruleApplied] || ruleApplied}`}>
          {RULE_LABELS[ruleApplied] || ruleApplied}
        </span>
      )}
      <div
        className={`message-bubble ${isUser ? "message-bubble--user" : "message-bubble--bot"}`}
        style={style}
      >
        {hasBilingual ? (
          <div className="message-bilingual">
            {meta.persona && (
              <p className="message-persona" dir="ltr">
                {meta.persona}
              </p>
            )}
            <p className="message-original" dir="rtl" lang={meta.language || "ar"}>
              {meta.original}
            </p>
            <div className="message-divider" aria-hidden="true" />
            <p className="message-translation" dir="ltr" lang="en">
              {meta.translation}
            </p>
          </div>
        ) : (
          content
        )}
      </div>
    </div>
  );
}
