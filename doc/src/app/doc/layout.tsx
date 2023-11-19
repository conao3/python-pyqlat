interface LayoutProps {
  children: React.ReactNode
}

export default function Layout(props: LayoutProps) {
  return (
    <div style={{color: 'red'}}>
      {props.children}
    </div>
  )
}
