import { shallowMount } from '@vue/test-utils'
import Cell from '@/components/Cell'

describe('Cell', () => {

  it('has different default color based on props.coordinate', () => {
    const evenCell = shallowMount(Cell)
    const evenColor = evenCell.element.style.backgroundColor
    const oddCell = shallowMount(Cell, {
      propsData: {
        coordinate: [0, 1]
      }
    })
    // console.log(evenCell.vm.coordinate)
    const oddColor = oddCell.element.style.backgroundColor
    expect(evenColor).not.toBe(oddColor)
  })

  it('contains an icon, if it has a queen', () => {  
    const wrapper = shallowMount(Cell)
    wrapper.setData({ hasQueen: true })
    expect(wrapper.findAll('.queen').length).toEqual(1)
  })

  it('changes color on click, if it has a queen', () => {
    const wrapper = shallowMount(Cell)
    wrapper.setData({ hasQueen: true })
    const baseColor = wrapper.element.style.backgroundColor
    wrapper.trigger('click')
    expect(wrapper.element.style.backgroundColor).not.toBe(baseColor)
  })

  it('returns to default color if clicked again', () => {
    const wrapper = shallowMount(Cell)
    wrapper.setData({ hasQueen: true })
    const baseColor = wrapper.element.style.backgroundColor
    wrapper.trigger('click')
    wrapper.trigger('click')
    expect(wrapper.element.style.backgroundColor).toBe(baseColor)
  })

  it('keeps color on click, if it doesn\'t have a queen', () => {
    const wrapper = shallowMount(Cell)
    wrapper.setData({ hasQueen: false })
    // console.log(`This has a queen ${wrapper.vm.hasQueen}`)
    const baseColor = wrapper.element.style.backgroundColor
    wrapper.trigger('click')
    expect(wrapper.element.style.backgroundColor).toBe(baseColor)
  })

})