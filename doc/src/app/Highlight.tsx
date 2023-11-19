interface HighlightProps {
  children: React.ReactNode
}

export function Highlight(props: HighlightProps) {
  return (
    <div
      style={{
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
        width: 'calc(100vw - var(--scrollbar))',
        marginLeft: 'calc(50% - (100vw - var(--scrollbar)) / 2)',
      }}
    >
      {props.children}
    </div>
  )
}
