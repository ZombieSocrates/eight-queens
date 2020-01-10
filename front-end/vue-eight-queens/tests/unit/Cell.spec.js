import { shallowMount } from '@vue/test-utils'
import Cell from '@/components/Cell'

describe('Cell', () => {
  it('changes color when clicked on, if it has a queen', () => {
    const wrapper = shallowMount(Cell, {
      setData: {
          hasQueen: true
      }
    })
    const baseColor = wrapper.element.style.backgroundColor
    console.log(`Original Color was ${baseColor}`)
    wrapper.trigger('click')
    expect(wrapper.element.style.backgroundColor).not.toBe(baseColor)
  })

  it('has different color dependent on value of props.coordinate', () => {
    const evenCell = shallowMount(Cell, {
      propsData: {
        coordinate: [0, 0]
      }
    })
    const evenColor = evenCell.element.style.backgroundColor
    const oddCell = shallowMount(Cell, {
      propsData: {
        coordinate: [0, 1]
      }
    })
    console.log(evenCell.vm.coordinate)
    const oddColor = oddCell.element.style.backgroundColor
    expect(evenColor).not.toBe(oddColor)
  })
})