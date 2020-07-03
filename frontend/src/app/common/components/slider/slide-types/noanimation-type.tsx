import React from "react";
import cn from 'classnames';

interface Props {
  slides: Object[],
  indexOfActiveSlide: number,
  size: Object,
  transparency: boolean,
}


export default function(props: Props)
{
  let animation = "noanimation" + (props.transparency? "-transparent": "")

  return (
    <div className="slider__wrapper" style={props.size}>
    {
      props.slides.map((slide, i) => (
        <div
          className={cn("slider__slide", "slider__slide_"+animation,
                        props.indexOfActiveSlide === i && 'slider__slide_' + animation + '_status_active')}
          key={i}
          style={props.size}
        >
          {slide}
        </div>
      ))
    }
    </div>
  )
}
