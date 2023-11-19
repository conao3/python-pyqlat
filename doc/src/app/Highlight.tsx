interface HighlightProps {
  children: React.ReactNode
}

export function Highlight(props: HighlightProps) {
  return (
    <div
      style={{
        position: 'relative',
      }}
    >
      <div
        style={{
          position: 'absolute',
          background: (
            [
              'radial-gradient(',
              'circle',
              'closest-side',
              'at 50% 25%',
              ',',
              [
                '#abdcff',
                '#0396ff 200%',
                'rgba(0, 0, 0, 0) 800%',
              ].join(','),
              ')',
            ].join(' ')
          ),
          height: '30rem',
          width: '100%',
        }}
      >
        {props.children}
      </div>
    </div>
  )
}
